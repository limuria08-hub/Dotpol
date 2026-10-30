import { test, expect, type Page } from '@playwright/test';

const API = 'http://127.0.0.1:8765';

async function makeProject(page: Page, name: string) {
  await page.goto('/');
  await expect(page.getByRole('status').first()).toContainText('Local research engine connected.');
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
  await expect(page.getByRole('status').first()).toContainText('Imported synthetic-budget.txt');

  await page.getByRole('checkbox', { name: /Evidence only/ }).check();
  const result = await ask(page, 'water budget');
  expect(result.ai_generated).toBe(false);
  expect(result.generation_method).toBe('extractive');
  expect(result.artifact.revision).toBe(1);
  expect(result.artifact.evidence[0].excerpt).toContain('120 units');

  const id: string = result.artifact.id;
  const projectId: string = result.artifact.project_id;
  await expect(page.locator('article.result')).toContainText('120 units');
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
  await expect(page.getByRole('status').first()).toContainText('Imported record.txt');
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
  await expect(second.getByRole('status').first()).toContainText('modified by another edit');
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

  // The visible upload button must be reachable by Tab; its hidden native
  // input is activated from that button and is not a competing tab stop.
  await page.getByRole('button', { name: title, exact: true }).focus();
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Import source' })).toBeFocused();
  expect(await page.evaluate(() =>
    document.documentElement.scrollWidth <= window.innerWidth + 1,
  )).toBeTruthy();
});
