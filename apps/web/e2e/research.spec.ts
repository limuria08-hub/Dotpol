import { test, expect, type Page } from '@playwright/test';

const API = 'http://127.0.0.1:8765';

async function makeProject(page: Page, name: string) {
  await page.goto('/');
  await expect(page.locator('p.status')).toContainText('Local research engine connected.');
  await page.getByRole('textbox', { name: 'New project name' }).fill(name);
  await page.getByRole('button', { name: '+ New project' }).click();
  await expect(page.getByRole('heading', { name })).toBeVisible();
  // Creating a project loads sources/artifacts asynchronously; a visible heading
  // does not mean the upload control has finished re-enabling.
  await expect(page.locator('input[type="file"]')).toBeEnabled();
}

async function ask(page: Page, question: string) {
  await page.getByRole('textbox', { name: 'Research question' }).fill(question);
  const response = page.waitForResponse(r =>
    r.url().includes('/research') && r.request().method() === 'POST',
  );
  await page.getByRole('button', { name: 'Ask AI' }).click();
  const reply = await response;
  expect(reply.ok()).toBeTruthy();
  return reply.json();
}

test('real browser: import → cited extract → same-ID edit → restart/reopen', async ({ page, request }) => {
  const title = 'P1 source journey ' + Date.now();
  await makeProject(page, title);

  const source = 'Synthetic public budget report\nWater budget: 120 units in 2026.\n';
  await page.locator('input[type="file"]').setInputFiles({
    name: 'synthetic-budget.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from(source),
  });
  await expect(page.locator('p.status')).toContainText('Imported synthetic-budget.txt');

  await page.getByRole('checkbox', { name: /Evidence only/ }).check();
  const result = await ask(page, 'water budget');
  expect(result.ai_generated).toBe(false);
  expect(result.generation_method).toBe('extractive');
  expect(result.artifact.revision).toBe(1);
  expect(result.artifact.evidence[0].excerpt).toContain('120 units');

  const id: string = result.artifact.id;
  const projectId: string = result.artifact.project_id;
  await expect(page.locator('article.result')).toContainText('120 units');
  // UI-04: this is the SAME persisted artifact opened from the real conversation.
  const openInWorkbench = page.getByRole('button', { name: `Open artifact ${id} in workbench` });
  await expect(openInWorkbench).toBeVisible();
  await openInWorkbench.click();
  await expect(page.locator('article.result')).toContainText('Water budget');
  const resize = page.getByRole('separator', { name: 'Resize conversation and artifact workbench' });
  await expect(resize).toBeVisible();
  await resize.focus();
  await expect(resize).toBeFocused();
  await page.keyboard.press('ArrowRight');
  await page.getByRole('button', { name: 'Edit in workbench', exact: true }).click();
  const revisedText = 'Human-reviewed summary: synthetic water budget is 120 units.';
  await page.getByLabel('Edit research artifact').fill(revisedText);
  await page.getByRole('button', { name: 'Save revision' }).click();
  await expect(page.locator('article.result')).toContainText('Revision 2 · Edited — citations need review');
  await expect(page.locator('article.result')).toContainText(revisedText);

  const stored = await request.get(`${API}/api/projects/${projectId}/artifacts/${id}`);
  expect(stored.ok()).toBeTruthy();
  const artifact = await stored.json();
  expect(artifact.id).toBe(id);
  expect(artifact.revision).toBe(2);
  expect(artifact.review_status).toBe('user-edited-unverified');
  expect(artifact.generation_method).toBe('extractive');
  expect(artifact.evidence).toEqual(result.artifact.evidence);

  // Reopening is through the actual persisted UI, not a test-only database fixture.
  await page.reload();
  await expect(page.getByRole('button', { name: title, exact: true })).toBeVisible();
  await page.getByRole('button', { name: title, exact: true }).click();
  await page.locator('.artifact-list').getByRole('button', { name: /water budget/ }).click();
  await expect(page.locator('article.result')).toContainText(revisedText);
  await expect(page.getByRole('button', { name: `Open artifact ${id} in workbench` })).toBeVisible();
  await page.locator('article.result').getByText('Revision history (2)').click();
  await expect(page.locator('.revision-entry')).toHaveCount(2);
  await expect(page.locator('.revision-entry').first()).toContainText('generated');
  await expect(page.locator('.revision-entry').last()).toContainText(revisedText);
});

test('no-model and no-evidence path abstains instead of inventing claims', async ({ page }) => {
  await makeProject(page, 'P1 no-evidence ' + Date.now());
  await expect(page.getByText('AI · model not configured')).toBeVisible();
  const result = await ask(page, 'unicorn budget comparison');
  expect(result.ai_generated).toBe(false);
  expect(result.has_evidence).toBe(false);
  expect(result.generation_method).toBe('no-evidence');
  expect(result.artifact.evidence).toEqual([]);
  await expect(page.locator('article.result')).toContainText('No matching evidence');
});

test('stale browser edit is rejected and cannot overwrite the newer revision', async ({ page, context, request }) => {
  const title = 'P1 revision race ' + Date.now();
  await makeProject(page, title);
  await page.locator('input[type="file"]').setInputFiles({
    name: 'record.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from('Synthetic public report: water budget is 88 units.'),
  });
  await expect(page.locator('p.status')).toContainText('Imported record.txt');
  const result = await ask(page, 'water budget');
  const artifactId: string = result.artifact.id;
  const projectId: string = result.artifact.project_id;
  const second = await context.newPage();
  await second.goto('/');
  await second.getByRole('button', { name: title, exact: true }).click();
  await second.locator('.artifact-list').getByRole('button', { name: /water budget/ }).click();
  await second.getByRole('button', { name: 'Edit in workbench', exact: true }).click();
  await second.getByLabel('Edit research artifact').fill('Stale second-tab edit');

  await page.getByRole('button', { name: 'Edit in workbench', exact: true }).click();
  await page.getByLabel('Edit research artifact').fill('First-tab accepted edit');
  await page.getByRole('button', { name: 'Save revision' }).click();
  await expect(page.locator('article.result')).toContainText('Revision 2 · Edited — citations need review');

  await second.getByRole('button', { name: 'Save revision' }).click();
  await expect(second.locator('p.status')).toContainText('modified by another edit');
  const stored = await request.get(`${API}/api/projects/${projectId}/artifacts/${artifactId}`);
  expect(stored.ok()).toBeTruthy();
  const artifact = await stored.json();
  expect(artifact.revision).toBe(2);
  expect(artifact.answer).toBe('First-tab accepted edit');
  await second.close();
});

test('narrow viewport retains keyboard-accessible uploads without horizontal overflow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const title = 'P1 mobile ' + Date.now();
  await makeProject(page, title);
  await expect(page.getByRole('heading', { name: 'Ask LiOS.Pol AI' })).toBeVisible();

  // Keyboard activation must open the native file chooser and complete an
  // actual source import (not just focus a hidden input programmatically).
  const importButton = page.getByRole('button', { name: 'Import source' });
  await expect(importButton).toBeEnabled();
  await importButton.focus();
  await expect(importButton).toBeFocused();
  const chooserPromise = page.waitForEvent('filechooser');
  await page.keyboard.press('Enter');
  const chooser = await chooserPromise;
  await chooser.setFiles({
    name: 'keyboard-source.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from('Synthetic keyboard source: local import verified.'),
  });
  await expect(page.locator('p.status')).toContainText('Imported keyboard-source.txt');
  expect(await page.evaluate(() =>
    document.documentElement.scrollWidth <= window.innerWidth + 1,
  )).toBeTruthy();
});


test('required OpenClaw gateway status is explicit, opt-in and credential-free', async ({ page }) => {
  let probeCount = 0;
  let reply = {
    component: 'openclaw', required_for_release: true, ready: false,
    status: 'not-installed', detail: 'OpenClaw CLI is not installed. Required integration is incomplete.',
  };
  await page.route(`${API}/api/openclaw/status`, async route => {
    probeCount += 1;
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ ...reply, secret: 'NEVER_SHOW_OPERATOR_TOKEN' }),
    });
  });
  await page.goto('/');
  const panel = page.getByRole('region', { name: 'Required OpenClaw gateway' });
  await expect(panel).toBeVisible();
  await expect(panel).toContainText('Required');
  await expect(panel).toContainText('Local gateway not checked');
  expect(probeCount).toBe(0); // Explicit probe only, not on initial page load.

  await panel.getByRole('button', { name: 'Check gateway' }).click();
  await expect(panel).toContainText('OpenClaw CLI is not installed');
  expect(probeCount).toBe(1);
  await expect(panel).not.toContainText('NEVER_SHOW_OPERATOR_TOKEN');

  reply = {
    component: 'openclaw', required_for_release: true, ready: true,
    status: 'gateway-healthy', detail: 'OpenClaw health RPC succeeded. Channels and tools not yet verified.',
  };
  await panel.getByRole('button', { name: 'Check gateway' }).click();
  await expect(panel).toContainText('OpenClaw health RPC succeeded');
  await expect(panel).not.toContainText('NEVER_SHOW_OPERATOR_TOKEN');
  expect(probeCount).toBe(2);

  await page.route(`${API}/api/openclaw/status`, route => route.abort('failed'));
  await panel.getByRole('button', { name: 'Check gateway' }).click();
  await expect(panel).toContainText('Could not verify the local OpenClaw gateway');
  await expect(panel.getByRole('button', { name: 'Check gateway' })).toBeEnabled();
});
