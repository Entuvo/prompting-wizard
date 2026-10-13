'use strict';
const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const list = value => Array.isArray(value) ? value : [];
const short = value => value ? String(value).slice(0,12) : 'not recorded';
let events;
let snapshot, projectId, selected={kind:'overview',id:''}, overlay={kind:'all',id:''}, connected=false, lastMessage=0, signature='';
const token = new URLSearchParams(location.hash.slice(1)).get('token') || sessionStorage.getItem('keelson-token') || '';
if(token) sessionStorage.setItem('keelson-token',token);
history.replaceState(null,'',location.pathname);
const button = (kind,id,label,classes='',pressed=false) => `<button type="button" data-key="${esc(kind+':'+id)}" class="${classes}" aria-pressed="${pressed}">${label}</button>`;
const tag = (text,cls='') => `<span class="tag ${cls}">${esc(text)}</span>`;
function project(){return snapshot?.projects.find(p=>p.id===projectId) || snapshot?.projects[0];}
function byId(key,id){return list(project()[key]).find(item=>item.id===id);}
function scope(){
  const p=project(), all=new Set(list(p.journeys).map(j=>j.id));
  let journeys=all, components=new Set(), edges=new Set();
  const kind=overlay.kind, item=byId({task:'tasks',milestone:'milestones',capability:'capabilities',journey:'journeys'}[kind],overlay.id);
  if(item){
    journeys=new Set(kind==='journey'?[item.id]:list(item.journeyIds));
    list(item.componentIds).forEach(i=>components.add(i)); list(item.edgeIds).forEach(i=>edges.add(i));
    if(kind==='milestone') list(item.taskIds).forEach(tid=>{
      const t=byId('tasks',tid); list(t?.journeyIds).forEach(i=>journeys.add(i));list(t?.componentIds).forEach(i=>components.add(i));list(t?.edgeIds).forEach(i=>edges.add(i));
    });
  }
  list(p.journeys).filter(j=>journeys.has(j.id)).forEach(j=>list(j.edgeIds).forEach(e=>edges.add(e)));
  list(p.edges).filter(e=>edges.has(e.id)).forEach(e=>{components.add(e.from);components.add(e.to);});
  if(kind==='all') list(p.components).forEach(c=>components.add(c.id));
  return {journeys,components,edges};
}
function evidenceStatus(e){return e ? `${e.result} · ${e.freshness}` : 'Unverified';}
function statusClass(e){return e?.freshness==='current' && e.result==='passed'?'pass':e?.freshness==='current'&&(e?.result==='failed'||e?.result==='changes requested'||e?.result==='blocked')?'fail':e?.freshness==='stale'||e?.freshness==='expired'?'warn':'';}
function journeyEvidence(journey,edge){
  return list(project().evidence).filter(e=>e.kind==='verification' && list(e.journeyIds).includes(journey) && (!edge || list(e.edgeIds).includes(edge))).sort((a,b)=>String(b.observedAt||b.startedAt||'').localeCompare(String(a.observedAt||a.startedAt||'')));
}
function edgeBadges(edge,s){
  return list(project().journeys).filter(j=>s.journeys.has(j.id)&&list(j.edgeIds).includes(edge.id)).map(j=>{
    const e=journeyEvidence(j.id,edge.id)[0];
    const blockers=list(project().tasks).filter(t=>(t.state==='blocked'||list(t.blockers).length)&&list(t.journeyIds).includes(j.id)&&list(t.edgeIds).includes(edge.id));
    return `<span class="edge-status ${blockers.length?'warn':statusClass(e)}">${esc(j.name)}: ${esc(evidenceStatus(e))}${blockers.length?` · Blocked by ${esc(blockers.map(t=>t.id).join(', '))}`:''}</span>`;
  }).join('') || '<span class="muted">Outside selected journeys</span>';
}
function gates(items){return list(items).length ? `<ul class="gates">${items.map(g=>`<li>${tag(g.satisfied?'Met':g.status==='blocked'?'Blocked':'Unverified',g.satisfied?'pass':'warn')} <strong>${esc(g.label)}</strong><span>${esc(g.reason)}</span></li>`).join('')}</ul>`:'<p class="muted">No acceptance predicates recorded.</p>';}
function taskLinks(tasks){return tasks.length?tasks.map(t=>button('task',t.id,`${esc(t.id)} · ${esc(t.name)} ${tag(t.state||'unknown')}`,'related')).join(''):'<p class="muted">No related tasks recorded.</p>';}
function evidenceDetails(e){
  if(!e)return '<p class="muted">No evidence recorded. No observation time is available.</p>';
  return `<article class="receipt"><h4>${esc(e.id)}</h4>${tag(evidenceStatus(e),statusClass(e))}
    <dl><dt>Evidence kind</dt><dd>${esc(e.kind)}</dd><dt>Evidence revision</dt><dd>${esc(e.revision||'Not recorded; see input hashes')}</dd>
    <dt>Evidence context</dt><dd>${esc(e.environment)}</dd><dt>Observed</dt><dd>${esc(e.observedAt||'No completed observation')}</dd>
    <dt>Source applicability</dt><dd>${esc(e.sourceApplicability)}</dd><dt>Expires</dt><dd>${esc(e.expiresAt||'No expiry recorded; runtime freshness not established')}</dd>
    <dt>Receipt</dt><dd><code>${esc(e.receipt)}</code></dd></dl>${e.note?`<p>${esc(e.note)}</p>`:''}
    ${e.kind==='review'?`<section aria-label="Review scope"><h5>Review scope</h5><p>${esc(e.reviewPurpose||'Purpose not recorded')}</p>
    <p>${esc(e.reviewSummary||'Review summary unavailable')}</p><h5>Review limits</h5>
    ${list(e.reviewLimits).length?`<ul>${e.reviewLimits.map(limit=>`<li>${esc(limit)}</li>`).join('')}</ul>`:'<p>Unverified: review limits unavailable.</p>'}</section>`:''}
    <details><summary>Covered inputs (${Object.keys(e.inputHashes||{}).length})</summary>${Object.entries(e.inputHashes||{}).map(([p,h])=>`<p><code>${esc(p)}</code> <code>${esc(short(h))}</code></p>`).join('')||'<p>Unbound legacy evidence.</p>'}</details></article>`;
}
function panel(){
  const p=project(), kind=selected.kind;
  const item=byId({task:'tasks',milestone:'milestones',component:'components',edge:'edges',journey:'journeys',capability:'capabilities',evidence:'evidence',workflow:'workflow'}[kind],selected.id);
  if(!item)return `<h2>Evidence & readiness</h2><p>Select a component, connection, task or milestone to inspect its scope and evidence.</p><h3>Release predicates</h3>${gates(p.releaseGates)}`;
  let html=`<h2>${esc(item.name||item.id)}</h2><p class="muted">${esc(kind)} · ${esc(item.id)}</p>${item.description?`<p>${esc(item.description)}</p>`:''}${item.implementationStatus?tag(item.implementationStatus):''}`, evidence=[];
  if(kind==='task'){
    html+=`<dl><dt>Task owner</dt><dd>${esc(item.owner||'Unassigned')}</dd><dt>Work claim</dt><dd>${esc(item.state||'unknown')}</dd><dt>Task / current revision</dt><dd>${esc(item.recordRevision||p.revision)}</dd></dl>`;
    if(item.nextAction)html+=`<p>Next: ${esc(item.nextAction)}</p>`;
    html+=list(item.blockers).map(b=>`<p class="blocker"><strong>${esc(b.owner)}</strong> · ${esc(b.action)}</p>`).join('');
    html+=`${item.source?`<p>Work record: <code>${esc(item.source)}</code></p>`:''}<h3>Depends on</h3>${taskLinks(list(item.dependsOn).map(id=>byId('tasks',id)).filter(Boolean))}`;
    evidence=list(item.evidenceIds).map(id=>byId('evidence',id));
  } else if(kind==='milestone'){
    html+=tag(item.status,item.status==='accepted'?'pass':'warn')+gates(item.gates);
    if(list(item.blockedTaskIds).length)html+=`<h3>Blocking tasks</h3>${taskLinks(item.blockedTaskIds.map(id=>byId('tasks',id)).filter(Boolean))}`;
    if(item.acceptance)html+=`<h3>Acceptance record</h3><p>${esc(item.acceptance.actor)} · ${esc(item.acceptance.at)} · revision ${esc(item.acceptance.revision)}. Current applicability: ${esc(item.status==='accepted'?'accepted':'not accepted')}.</p>`;
    html+=`<h3>Tasks</h3>${taskLinks(list(item.taskIds).map(id=>byId('tasks',id)).filter(Boolean))}`;
    evidence=list(item.gates).filter(g=>g.evidenceId).map(g=>byId('evidence',g.evidenceId));
  } else if(kind==='edge'||kind==='component'){
    const field=kind==='edge'?'edgeIds':'componentIds';
    html+=`<h3>Related tasks · all journeys</h3>${taskLinks(list(p.tasks).filter(t=>list(t[field]).includes(item.id)))}`;
    evidence=list(p.evidence).filter(e=>list(e[field]).includes(item.id));
    if(kind==='component')html+=`<h3>Source mapping</h3>${list(item.sources).map(s=>`<p><code>${esc(s)}</code></p>`).join('')||'<p>External component; no local source path.</p>'}`;
  } else if(kind==='workflow'){
    html+=`<p>Project-wide workflow record.</p>${taskLinks(list(item.taskIds).map(id=>byId('tasks',id)).filter(Boolean))}`;
    evidence=list(item.evidenceIds).map(id=>byId('evidence',id));
  } else if(kind==='evidence') evidence=[item];
  else evidence=list(p.evidence).filter(e=>list(e.journeyIds).some(id=>kind==='journey'?id===item.id:list(item.journeyIds).includes(id)));
  html+='<h3>Evidence</h3>'+(evidence.length?[...new Map(evidence.filter(Boolean).map(e=>[e.id,e])).values()].map(evidenceDetails).join(''):evidenceDetails(null));
  return html;
}
function render(force=false){
  const p=project();if(!p)return;
  const dataSignature=JSON.stringify(p,(key,value)=>key==='collectedAt'?undefined:value)+JSON.stringify([selected,overlay]);
  if(!force&&dataSignature===signature)return; signature=dataSignature;
  const active=document.activeElement, focusKey=active?.dataset.key, focusIndex=focusKey?[...document.querySelectorAll('[data-key]')].filter(e=>e.dataset.key===focusKey).indexOf(active):0;
  const open=[...document.querySelectorAll('details[open]')].map(e=>e.dataset.detail).filter(Boolean);
  const s=scope();
  $('#app').innerHTML=`<div class="project-heading"><div><h1>${esc(p.name)}</h1><p>${p.synthetic?'<strong class="warn">Synthetic acceptance fixture</strong> · ':''}Source revision <code>${esc(short(p.revision))}</code> · Evidence verified by input hashes</p></div>${tag(p.releaseReady?'Release predicates met':'Release not qualified',p.releaseReady?'pass':'warn')}</div>
    <p class="status-summary">${list(p.evidence).filter(e=>e.kind==='verification'&&e.freshness==='current'&&e.result==='passed').length} current scoped checks · ${list(p.tasks).filter(t=>t.state==='blocked'||list(t.blockers).length).length} tasks with blockers · ${list(p.milestones).filter(m=>m.status==='unverified').length} unverified milestones. Passing local checks qualify only their recorded scope.</p>
    ${p.error?`<p class="alert">${esc(p.error)}</p>`:''}${list(p.warnings).map(w=>`<p class="alert">${esc(w)}</p>`).join('')}
    <section aria-labelledby="milestones-title"><div class="section-title"><h2 id="milestones-title">Milestones</h2><span>Accepted outcomes, backed by gates</span></div><div class="milestones">${list(p.milestones).map(m=>button('milestone',m.id,`<strong>${esc(m.name)}</strong><span>${esc(m.id)} · ${esc(m.status)}</span>`,'milestone',overlay.kind==='milestone'&&overlay.id===m.id)).join('')||'<p class="muted">No milestone gates recorded.</p>'}</div></section>
    ${p.scopeNote?`<p class="scope-note">${esc(p.scopeNote)}</p>`:''}<a class="evidence-jump" href="#evidence-panel">View selected evidence</a><div class="workspace"><div class="main-column"><section id="architecture" tabindex="-1" aria-labelledby="architecture-title"><div class="section-title"><h2 id="architecture-title">Architecture</h2>${button('all','all','Show all','reset',overlay.kind==='all')}</div>
    ${list(p.capabilities).length>8?`<details data-detail="capabilities"><summary>Capability overlays (${p.capabilities.length}) · ${esc(overlay.kind==='capability'?byId('capabilities',overlay.id)?.name:'choose a capability')}</summary>`:''}<div class="controls"><span>Capabilities</span>${list(p.capabilities).map(c=>button('capability',c.id,esc(c.name),'capability',list(c.journeyIds).some(id=>s.journeys.has(id)))).join('')}</div>${list(p.capabilities).length>8?'</details>':''}
    ${list(p.journeys).length>8?`<details data-detail="journeys"><summary>Journey overlays (${p.journeys.length}) · ${esc(overlay.kind==='journey'?byId('journeys',overlay.id)?.name:'choose a journey')}</summary>`:''}<div class="controls"><span>Journeys</span>${list(p.journeys).map(j=>button('journey',j.id,esc(j.name),'journey',s.journeys.has(j.id))).join('')||'<span>No journeys mapped</span>'}</div>${list(p.journeys).length>8?'</details>':''}
    <p class="legend">Blue dashed border: selected scope · Dark border: inspected item · Work labels: recorded claims</p>
    <div class="canvas"><svg id="connections" aria-hidden="true"></svg><div class="nodes">${list(p.components).map((c,i)=>{
      const tasks=list(p.tasks).filter(t=>list(t.componentIds).includes(c.id));
      const checked=list(p.evidence).some(e=>e.kind==='verification'&&list(e.componentIds).includes(c.id)&&e.freshness==='current'&&e.result==='passed');
      return button('component',c.id,`<strong>${esc(c.name)}</strong><span>${esc(c.implementationStatus||c.id)}</span>${tag(checked?'Scoped check passed':'Unverified behavior',checked?'pass':'')}<small>${tasks.length} related tasks · ${tasks.filter(t=>t.state==='blocked'||list(t.blockers).length).length} blocked</small>`,`component ${s.components.has(c.id)?'in-scope':''} ${selected.kind==='component'&&selected.id===c.id?'inspected':''}`);
    }).join('')}</div></div>
    <div class="edge-list" aria-label="Connection status by journey">${list(p.edges).filter(e=>overlay.kind==='all'||s.edges.has(e.id)).map(e=>`<div class="edge-row ${s.edges.has(e.id)?'in-scope':''}">${button('edge',e.id,`${esc(e.name)} <small>${esc(e.from)} → ${esc(e.to)}</small>`,selected.kind==='edge'&&selected.id===e.id?'inspected':'')}<div>${edgeBadges(e,s)}</div></div>`).join('')}</div></section>
    <section><div class="section-title"><h2>Tasks</h2><span>Work state is a claim; evidence qualifies behavior</span></div><div class="tasks">${list(p.tasks).map(t=>button('task',t.id,`<span><strong>${esc(t.id)} · ${esc(t.name)}</strong><small>${esc(t.owner||'Unassigned')} · ${list(t.milestoneIds).map(esc).join(', ')||'No milestone'}</small></span><span>${tag(t.state||'unknown',t.state==='blocked'?'warn':'')}${list(t.blockers).map(b=>`<small>${esc(b.owner)}: ${esc(b.action)}</small>`).join('')}</span>`,'task '+(overlay.kind==='task'&&overlay.id===t.id?'inspected':''))).join('')||'<p class="muted">No mapped tasks. Legacy work records appear below.</p>'}</div></section></div>
    <aside id="evidence-panel" tabindex="-1" aria-label="Evidence detail"><a class="back-canvas" href="#architecture">Back to architecture</a>${panel()}</aside></div>
    <section class="workflow"><div class="section-title"><h2>Keelson workflow</h2><span>Project-wide · separate from product behavior</span></div><div class="workflow-strip">${list(p.workflow).map(w=>button('workflow',w.id,`<strong>${esc(w.name)}</strong><small>${list(w.taskIds).map(esc).join(', ')||'No task mapping'}</small><span>${list(w.evidenceIds).map(id=>evidenceStatus(byId('evidence',id))).map(esc).join(' / ')||'No evidence linked'}</span>`,'workflow-item')).join('')||'<p>No workflow stages mapped. Receipts below remain available.</p>'}</div>
    <details data-detail="receipts"><summary>All receipts (${list(p.evidence).length}) · includes unmapped history</summary><div class="receipt-index">${list(p.evidence).map(e=>button('evidence',e.id,`<span>${esc(e.unit||e.id)}</span>${tag(evidenceStatus(e),statusClass(e))}`,'receipt-link')).join('')||'<p>No receipts found.</p>'}</div></details>
    ${list(p.unmappedUnits).length?`<details data-detail="units"><summary>Unmapped work-store units (${p.unmappedUnits.length})</summary>${p.unmappedUnits.map(u=>`<p>${esc(u.id)} · ${esc(u.state)} · ${esc(u.brief)}</p>`).join('')}</details>`:''}
    <details data-detail="checkpoint"><summary>Current project checkpoint</summary><pre>${esc(p.checkpoint||'No checkpoint configured.')}</pre></details>
    <details data-detail="roots"><summary>Record locations</summary><p>Engineering: <code>${esc(p.engineeringRoot)}</code></p><p>Private records: <code>${esc(p.recordsRoot)}</code></p></details></section>
    <footer>Read-only local view · Records collected every 2 seconds · Process availability does not prove a working user journey</footer>`;
  list(p.components).forEach((c,i)=>{
    const node=[...document.querySelectorAll('.component')][i];
    node.style.gridColumn=String((c.column ?? i%3)+1);node.style.gridRow=String((c.row ?? Math.floor(i/3))+1);
  });
  document.querySelectorAll('details').forEach(d=>{if(open.includes(d.dataset.detail))d.open=true;});
  if(focusKey){const nodes=[...document.querySelectorAll('[data-key]')].filter(e=>e.dataset.key===focusKey);(nodes[focusIndex]||nodes[0])?.focus({preventScroll:true});}
  requestAnimationFrame(drawConnections);
}
function drawConnections(){
  const p=project(),svg=$('#connections');if(!svg)return;
  const area=svg.getBoundingClientRect(),s=scope();
  svg.setAttribute('viewBox',`0 0 ${area.width} ${area.height}`);
  let markup='<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>';
  for(const [index,e] of list(p.edges).entries()){
    const from=[...document.querySelectorAll('.component')].find(n=>n.dataset.key==='component:'+e.from),to=[...document.querySelectorAll('.component')].find(n=>n.dataset.key==='component:'+e.to);if(!from||!to)continue;
    if(overlay.kind!=='all'&&!s.edges.has(e.id))continue;
    const a=from.getBoundingClientRect(),b=to.getBoundingClientRect();
    const readings=list(p.journeys).filter(j=>s.journeys.has(j.id)&&list(j.edgeIds).includes(e.id)).map(j=>journeyEvidence(j.id,e.id)[0]);
    const cls=readings.length&&readings.every(v=>statusClass(v)==='pass')?'pass':readings.some(v=>statusClass(v)==='fail')?'fail':'';
    const mobile=window.matchMedia('(max-width:540px)').matches;
    const lane=5+(index%4)*8;
    const path=mobile?`M ${a.left-area.left} ${a.top+a.height/2-area.top} H ${lane} V ${b.top+b.height/2-area.top} H ${b.left-area.left-5}`:`M ${a.left-area.left} ${a.top+a.height/2-area.top} H ${a.left-area.left-12} V ${a.top-area.top-16} H ${lane} V ${b.top-area.top-16} H ${b.left-area.left-12} V ${b.top+b.height/2-area.top} H ${b.left-area.left-5}`;
    markup+=`<path data-edge="${esc(e.id)}" class="connector ${cls}" d="${path}" marker-end="url(#arrow)"/>`;
  }
  svg.innerHTML=markup;
}
function connection(){
  const p=project(),collectionTime=Date.parse(snapshot?.collectedAt||'');
  const historical=!Number.isFinite(collectionTime)||Date.now()-collectionTime>12000||!connected||p?.historical||snapshot?.error||Date.now()-lastMessage>12000;
  $('#connection').className=historical?'historical':'';
  const time=p?.collectedAt||snapshot?.collectedAt;
  $('#connection').textContent=(historical?'Disconnected or collection unavailable — all displayed records are historical. ':'Connected · local records, not live product-health probes. ')+(time?'Last collection '+new Date(time).toLocaleTimeString()+'. ':'')+(snapshot?.error||p?.error||'');
  document.body.classList.toggle('historical',Boolean(historical));
}
function receive(data){
  snapshot=data;lastMessage=Date.now();connected=true;
  if(!snapshot.projects.some(p=>p.id===projectId))projectId=snapshot.projects[0]?.id;
  const select=$('#project');
  const options=snapshot.projects.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}${p.synthetic?' (synthetic)':''}</option>`).join('');
  if(select.innerHTML!==options)select.innerHTML=options;
  select.value=projectId;render();connection();
}
$('#project').addEventListener('change',e=>{projectId=e.target.value;selected={kind:'overview',id:''};overlay={kind:'all',id:''};render(true);connection();});
$('#app').addEventListener('click',e=>{
  const target=e.target.closest('[data-key]');if(!target)return;
  const colon=target.dataset.key.indexOf(':'),kind=target.dataset.key.slice(0,colon),id=target.dataset.key.slice(colon+1);
  selected={kind,id};if(['all','task','milestone','journey','capability'].includes(kind))overlay={kind,id};
  render(true);$('#announcement').textContent=`Showing ${kind} ${id} evidence.`;
});
window.addEventListener('resize',()=>requestAnimationFrame(drawConnections));
setInterval(connection,2000);
async function start(){
  try{
    const response=await fetch('/api/snapshot',{headers:{Authorization:'Bearer '+token}});
    if(!response.ok)throw Error('Open the authenticated dashboard URL printed by the launcher.');
    receive(await response.json());
    events?.close();
    events=new EventSource('/api/events?token='+encodeURIComponent(token));
    events.addEventListener('snapshot',e=>{try{receive(JSON.parse(e.data));}catch{connected=false;connection();}});
    events.onerror=()=>{connected=false;connection();};
  }catch(e){$('#app').textContent=e.message;connected=false;connection();}
}
window.addEventListener('offline',()=>{events?.close();connected=false;connection();});
window.addEventListener('online',start);
start();
