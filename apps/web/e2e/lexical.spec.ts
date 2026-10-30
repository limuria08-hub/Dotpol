import {test,expect,type Page} from '@playwright/test';

const API='http://127.0.0.1:8765';

async function createArtifact(page:Page){
 const title='P1 Lexical editor '+Date.now();
 await page.goto('/');
 await expect(page.locator('p.status')).toContainText('Local research engine connected.');
 await page.getByRole('textbox',{name:'New project name'}).fill(title);
 await page.getByRole('button',{name:'+ New project'}).click();
 await page.locator('input[type="file"]').setInputFiles({
  name:'verified-report.txt',mimeType:'text/plain',
  buffer:Buffer.from('Synthetic public transport budget is 56 units in 2026.'),
 });
 await expect(page.locator('p.status')).toContainText('Imported verified-report.txt');
 await page.getByRole('checkbox',{name:/Evidence only/}).check();
 const response=page.waitForResponse(r=>r.url().includes('/research')&&r.request().method()==='POST');
 await page.getByRole('textbox',{name:'Research question'}).fill('transport budget');
 await page.getByRole('button',{name:'Ask AI'}).click();
 const result=await (await response).json();
 await expect(page.locator('article.result')).toContainText('56 units');
 return {title,artifact:result.artifact};
}

test('Lexical editor persists multiline plain text under the same Artifact and evidence IDs',async({page,request})=>{
 const {title,artifact}=await createArtifact(page);
 const id:string=artifact.id,pid:string=artifact.project_id;
 await page.getByRole('button',{name:'Edit in workbench'}).click();
 const editor=page.getByRole('textbox',{name:'Edit research artifact'});
 await expect(editor).toBeVisible();
 const revised='Researcher summary: 56 units.\nSecond line. 🌐\n<em>literal text, not HTML</em>';
 await editor.fill(revised);
 await expect(page.getByRole('button',{name:'Save revision'})).toBeEnabled();
 await page.getByRole('button',{name:'Save revision'}).click();
 await expect(page.locator('article.result')).toContainText('Revision 2');
 const stored=await request.get(`${API}/api/projects/${pid}/artifacts/${id}`);
 expect(stored.ok()).toBe(true);
 const saved=await stored.json();
 expect(saved.id).toBe(id);
 expect(saved.revision).toBe(2);
 expect(saved.answer).toBe(revised);
 expect(saved.evidence).toEqual(artifact.evidence);
 expect(saved.review_status).toBe('user-edited-unverified');
 await expect(page.locator('article.result').locator('em')).toHaveCount(0);
 // The exported JSON must use the exact canonical revised Artifact.
 const downloadPromise=page.waitForEvent('download');
 await page.getByRole('button',{name:'Export JSON'}).click();
 const download=await downloadPromise;
 const fs=await import('node:fs/promises');
 const exported=JSON.parse(await fs.readFile(await download.path(),'utf8'));
 expect(exported.id).toBe(id);
 expect(exported.answer).toBe(revised);
 expect(exported.evidence).toEqual(artifact.evidence);
 await page.reload();
 await page.getByRole('button',{name:title,exact:true}).click();
 await page.locator('.artifact-list').getByRole('button',{name:/transport budget/}).click();
 await expect(page.locator('article.result')).toContainText('Second line. 🌐');
 await expect(page.locator('.revision-entry')).toHaveCount(0);
 await page.locator('article.result').getByText('Revision history (2)').click();
 await expect(page.locator('.revision-entry')).toHaveCount(2);
});

test('Lexical preserves unsaved text on cancellation and prevents oversized UTF-8 saves',async({page,request})=>{
 const {artifact}=await createArtifact(page);
 await page.getByRole('button',{name:'Edit in workbench'}).click();
 const editor=page.getByRole('textbox',{name:'Edit research artifact'});
 await editor.fill('Discard this unsaved change');
 await page.getByRole('button',{name:'Cancel',exact:true}).click();
 await expect(page.locator('article.result')).not.toContainText('Discard this unsaved change');
 await page.getByRole('button',{name:'Edit in workbench'}).click();
 const input=page.getByRole('textbox',{name:'Edit research artifact'});
 await expect(input).toContainText('56 units');
 await input.fill('🌐'.repeat(25001));
 await expect(page.getByRole('button',{name:'Save revision'})).toBeDisabled();
 await expect(page.getByRole('status')).toContainText('Shorten report before saving');
 await input.fill('Human verified excerpt only.');
 await expect(page.getByRole('button',{name:'Save revision'})).toBeEnabled();
 await page.getByRole('button',{name:'Save revision'}).click();
 const stored=await request.get(`${API}/api/projects/${artifact.project_id}/artifacts/${artifact.id}`);
 expect((await stored.json()).revision).toBe(2);
});
