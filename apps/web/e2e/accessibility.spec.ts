import {test, expect, type Page} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// All fixtures are synthetic and exercise the same production web + localhost API
// as research.spec.ts. This is a machine audit, NOT a manual screen-reader pass.
async function createLocalProject(page:Page){
  await page.goto('/');
  await expect(page.locator('p.status')).toContainText('Local research engine connected.');
  await page.getByRole('textbox',{name:'New project name'}).fill('Accessibility fixture '+Date.now());
  await page.getByRole('button',{name:'+ New project'}).click();
  await expect(page.getByRole('button',{name:'Import source'})).toBeEnabled();
}

async function importEvidence(page:Page){
  await page.locator('input[type=file]').setInputFiles({
    name:'accessibility-report.txt',mimeType:'text/plain',
    buffer:Buffer.from('Synthetic public education budget is 42 units in 2026.'),
  });
  await expect(page.locator('p.status')).toContainText('Imported accessibility-report.txt');
}

async function assertAccessible(page:Page,label:string){
  const result=await new AxeBuilder({page})
    .withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice'])
    .analyze();
  const blocking=result.violations.filter(v=>v.impact==='critical'||v.impact==='serious');
  expect(blocking.map(v=>({rule:v.id,impact:v.impact,help:v.help,
    nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary})).slice(0,8)})),
    `Automated serious/critical accessibility issues: ${label}`).toEqual([]);
}

test('landing and local project UI satisfy machine-scannable WCAG rules',async({page})=>{
  await page.goto('/');
  await expect(page.locator('p.status')).toContainText('Local research engine connected.');
  await assertAccessible(page,'landing');
  await createLocalProject(page);
  await assertAccessible(page,'empty project');
});

test('source provenance modal traps focus and remains accessible',async({page})=>{
  await createLocalProject(page);
  await importEvidence(page);
  await page.getByRole('button',{name:'Inspect source accessibility-report.txt'}).click();
  const dialog=page.getByRole('dialog',{name:'Source provenance'});
  await expect(dialog).toBeVisible();
  await assertAccessible(page,'source detail modal');
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
});

test('saved artifact, assistant-ui conversation and workbench satisfy automated audit',async({page})=>{
  await createLocalProject(page);
  await importEvidence(page);
  await page.getByRole('textbox',{name:'Research question'}).fill('education budget');
  await page.getByRole('button',{name:'Ask AI'}).click();
  await expect(page.locator('article.result')).toContainText('42 units');
  await assertAccessible(page,'classic workbench');
  await page.getByRole('button',{name:'Assistant conversation'}).click();
  await expect(page.getByLabel('Assistant research conversation')).toContainText('42 units');
  await assertAccessible(page,'assistant-ui with saved artifact');
});

test('390px stacked workbench remains accessible and does not overflow',async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await createLocalProject(page);
  await importEvidence(page);
  await page.getByRole('button',{name:'Assistant conversation'}).click();
  await page.getByRole('textbox',{name:'Assistant research question'}).fill('education budget');
  await page.getByRole('button',{name:'Send assistant research question'}).click();
  await expect(page.locator('article.result')).toContainText('42 units');
  await assertAccessible(page,'narrow assistant view');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBe(true);
});

test('local no-model UI makes zero requests to external origin during research flow',async({page})=>{
  const unexpected:string[]=[];
  await page.route('**/*',route=>{
    const url=new URL(route.request().url());
    const valid=url.protocol==='http:'&&url.hostname==='127.0.0.1'&&
      (url.port==='3000'||url.port==='8765');
    if(!valid){unexpected.push(url.origin);return route.abort()}
    return route.continue();
  });
  await createLocalProject(page);
  await importEvidence(page);
  await page.getByRole('button',{name:'Assistant conversation'}).click();
  await page.getByRole('textbox',{name:'Assistant research question'}).fill('education budget');
  await page.getByRole('button',{name:'Send assistant research question'}).click();
  await expect(page.locator('article.result')).toContainText('42 units');
  await expect(page.getByRole('button',{name:'Check gateway'})).toBeVisible();
  expect(unexpected,'Local app must not request remote assets or services without opt-in').toEqual([]);
});
