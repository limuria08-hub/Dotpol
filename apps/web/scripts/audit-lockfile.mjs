// Local, read-only licence metadata inventory from the committed npm lockfile.
// This does not claim legal clearance; restricted terms remain review gates.
import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const lock=JSON.parse(fs.readFileSync(path.join(root,'package-lock.json'),'utf8'));
const rootPkg=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
const entries=Object.entries(lock.packages||{}).filter(([key])=>key!=='');

function equal(a,b){
 const sorted=o=>JSON.stringify(Object.entries(o).sort(([x],[y])=>x.localeCompare(y)));
 return sorted(a)===sorted(b);
}
if(lock.lockfileVersion!==3||lock.name!==rootPkg.name||
   !equal(lock.packages[''].dependencies||{},rootPkg.dependencies||{})||
   !equal(lock.packages[''].devDependencies||{},rootPkg.devDependencies||{})){
 throw new Error('Dependency lock does not match the authored manifest');
}
const rows=entries.map(([location,meta])=>{
 const name=location.replace(/^.*node_modules\//,'');
 const license=String(meta.license||'UNKNOWN');
 const review=/(LGPL|GPL|AGPL|MPL|CC-BY|UNKNOWN)/i.test(license);
 return {name,version:meta.version,license,scope:meta.dev?'development':'runtime',
   optional:!!meta.optional,platforms:meta.os||[],license_review_required:review};
}).sort((a,b)=>a.name.localeCompare(b.name));
const missing=rows.filter(x=>x.license==='UNKNOWN');
const review=rows.filter(x=>x.license_review_required);
fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','license-inventory.json'),
 JSON.stringify({generated_from:'apps/web/package-lock.json',package_count:rows.length,
    manually_review:review,packages:rows},null,2)+'\n');
console.log('Locked npm packages:',rows.length);
console.log('Packages requiring licence/asset review:',review.length);
console.log('Licence review entries:',review.map(x=>x.name+' ('+x.license+')').join('; '));
if(missing.length)throw new Error('Locked packages have no licence metadata: '+missing.map(x=>x.name).join(', '));
// Do not silently accept nonpermissive licences. Report for legal/NOTICE
// review while keeping the machine integrity gate separate from legal signoff.
