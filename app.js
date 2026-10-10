/* AI Transformation Navigator — standalone GitHub Pages edition.
   Transparent educational model translated from reference-python/engine.py.
   All calculations execute locally; no API requests or model training. */
'use strict';
const DIMENSIONS = [
  {key:'Data & governance',weight:.25,short:'Data & governance',axis:'Data governance'},
  {key:'Technology infrastructure',weight:.20,short:'Technology infrastructure',axis:'Technology'},
  {key:'Process readiness',weight:.20,short:'Process readiness',axis:'Processes'},
  {key:'People & skills',weight:.20,short:'People & skills',axis:'People & skills'},
  {key:'Responsible AI & risk',weight:.15,short:'Responsible AI & risk',axis:'Responsible AI'}
];
const SECTORS = ['Manufacturing','Financial services','Professional services','Retail & e-commerce','Energy & infrastructure'];
const USE_CASES = [
  {name:'Enterprise knowledge assistant',category:'Knowledge management',description:'Find answers in approved internal documents with traceable sources.',impact:4.1,ease:4.4,required_readiness:38,sectors:SECTORS,risk:'Medium',guardrail:'Apply access controls, source citations and human review for critical answers.',kpi:'Time to locate a verified answer'},
  {name:'Document processing automation',category:'Operations',description:'Extract and validate invoice, form or operational document data.',impact:4.3,ease:4.2,required_readiness:45,sectors:['Manufacturing','Financial services','Retail & e-commerce','Energy & infrastructure'],risk:'Medium',guardrail:'Set confidence thresholds, exception queues and audit logs.',kpi:'Minutes per document processed'},
  {name:'Research & intelligence copilot',category:'Strategy',description:'Summarize public market, policy and competitor research for analyst review.',impact:4.0,ease:4.5,required_readiness:32,sectors:SECTORS,risk:'Medium',guardrail:'Display citations and require analysts to verify material claims.',kpi:'Analyst hours per research brief'},
  {name:'Predictive maintenance analytics',category:'Industrial operations',description:'Forecast equipment downtime using verified maintenance and sensor data.',impact:4.8,ease:2.8,required_readiness:70,sectors:['Manufacturing','Energy & infrastructure'],risk:'High',guardrail:'Validate sensor coverage and backtest models before operational use.',kpi:'Unplanned downtime hours'},
  {name:'Customer service triage',category:'Customer experience',description:'Route customer inquiries and draft replies for staff approval.',impact:4.1,ease:3.8,required_readiness:50,sectors:['Financial services','Professional services','Retail & e-commerce'],risk:'Medium',guardrail:'Keep humans involved in complaints and sensitive customer interactions.',kpi:'First-response time'},
  {name:'Demand forecasting support',category:'Planning',description:'Forecast demand and compare operational planning scenarios.',impact:4.6,ease:3.1,required_readiness:64,sectors:['Manufacturing','Retail & e-commerce','Energy & infrastructure'],risk:'Medium',guardrail:'Backtest accuracy and allow planners to override recommendations.',kpi:'Forecast error / MAPE'}
];
const weights = [{name:'Business impact',weight:35},{name:'Implementation ease',weight:30},{name:'Sector relevance',weight:20},{name:'Readiness fit',weight:15}];
const $=id=>document.getElementById(id);
const state={company:'Northstar Manufacturing',sector:'Manufacturing',employees:420,ratings:{'Data & governance':2,'Technology infrastructure':3,'Process readiness':3,'People & skills':3,'Responsible AI & risk':3},roi:{affected:40,hours:2,cost:35,weeks:48,upfront:40000,recurring:18000,adoption:60},selectedCase:'',view:'diagnose'};
const round1=v=>Math.round((v+Number.EPSILON)*10)/10;
const usd=v=>(v<0?'−':'')+'$'+Math.round(Math.abs(v)).toLocaleString('en-US');
const num=v=>Math.round(v).toLocaleString('en-US');
const pct=v=>(Number.isFinite(v)?`${v.toFixed(1)}%`:'N/A');
const esc=s=>String(s).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const value=(id,defaultVal=0)=>{const n=Number($(id).value);return Number.isFinite(n)?n:defaultVal};
const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
function scoreReadiness(){return round1(DIMENSIONS.reduce((sum,d)=>sum+(state.ratings[d.key]-1)/4*100*d.weight,0))}
function band(score){return score<35?'Foundational':score<65?'Developing':'Scaling-ready'}
function rankCases(score){return USE_CASES.map(c=>{const sectorFit=c.sectors.includes(state.sector)?5:2;const gap=Math.max(0,c.required_readiness-score);const readinessFit=Math.max(1,5-gap/15);const priority=round1(20*(.35*c.impact+.30*c.ease+.20*sectorFit+.15*readinessFit));return {...c,sectorFit,readinessFit,priority}}).sort((a,b)=>b.priority-a.priority)}
function roiModel(){const p=state.roi;const hours=p.affected*p.hours*p.weeks*p.adoption/100;const gross=hours*p.cost;const annualNet=gross-p.recurring;const firstYear=annualNet-p.upfront;const roi=p.upfront>0?firstYear/p.upfront*100:null;const payback=annualNet>0?12*p.upfront/annualNet:null;return {hours,gross,annualNet,firstYear,roi,payback,cumulative:[-p.upfront,-p.upfront+annualNet,-p.upfront+2*annualNet,-p.upfront+3*annualNet]}}
function dimensionMarkup(){return DIMENSIONS.map(d=>`<div class="readiness-item"><div class="readiness-label"><strong>${esc(d.short)}</strong><span>${state.ratings[d.key]} / 5</span></div><div class="readiness-input"><input type="range" min="1" max="5" step="1" value="${state.ratings[d.key]}" data-dimension="${esc(d.key)}" aria-label="${esc(d.short)} maturity" style="--fill:${(state.ratings[d.key]-1)*25}%" /><output>${state.ratings[d.key]}</output></div><div class="readiness-weight">${Math.round(d.weight*100)}% assessment weight</div></div>`).join('')}
function setupControls(){
  $('dimension-controls').innerHTML=dimensionMarkup();
  $('dimension-controls').querySelectorAll('input[data-dimension]').forEach(input=>input.addEventListener('input',()=>{state.ratings[input.dataset.dimension]=Number(input.value);input.style.setProperty('--fill',`${(Number(input.value)-1)*25}%`);input.closest('.readiness-item').querySelector('output').textContent=input.value;input.closest('.readiness-item').querySelector('.readiness-label span').textContent=`${input.value} / 5`;render()}));
  $('company').addEventListener('input',e=>{state.company=e.target.value.trim().slice(0,70)||'Unnamed organization';renderReport()});
  $('sector').addEventListener('change',e=>{state.sector=e.target.value;render()});
  $('employees').addEventListener('change',e=>{const n=clamp(Math.round(Number(e.target.value)||1),1,1000000);e.target.value=n;state.employees=n;state.roi.affected=Math.min(state.roi.affected,n);$('affected').max=n;$('affected').value=state.roi.affected;render()});
  document.querySelectorAll('.nav-link').forEach(btn=>btn.addEventListener('click',()=>activate(btn.dataset.view,true)));
  ['affected','hours','cost-hour','weeks','upfront','recurring','adoption'].forEach(id=>$(id).addEventListener('input',()=>{
    const maps={'affected':'affected','hours':'hours','cost-hour':'cost','weeks':'weeks','upfront':'upfront','recurring':'recurring','adoption':'adoption'};
    const max={affected:state.employees,hours:168,cost:1000000,weeks:52,upfront:100000000,recurring:100000000,adoption:100}[id];
    const min=0;state.roi[maps[id]]=clamp(value(id),min,max);
    if(id==='adoption'){$('adoption-display').textContent=`${state.roi.adoption}%`;$(id).style.setProperty('--fill',`${state.roi.adoption}%`)}
    renderRoi();renderReport();
  }));
  ['affected','hours','cost-hour','weeks','upfront','recurring'].forEach(id=>$(id).addEventListener('change',()=>{const maps={'affected':'affected','hours':'hours','cost-hour':'cost','weeks':'weeks','upfront':'upfront','recurring':'recurring'};$(id).value=state.roi[maps[id]]}));
  $('usecase').addEventListener('change',e=>{state.selectedCase=e.target.value;renderReport()});
  $('download-report').addEventListener('click',downloadMarkdown);
  $('print-report').addEventListener('click',()=>{activate('report',false);window.print()});
  window.addEventListener('hashchange',()=>{const hash=location.hash.replace('#','');if(['diagnose','prioritize','roi','report'].includes(hash))activate(hash,false)});
}
function activate(name,scroll){if(!['diagnose','prioritize','roi','report'].includes(name))return;state.view=name;document.querySelectorAll('.view').forEach(view=>{const show=view.id===`view-${name}`;view.hidden=!show;view.classList.toggle('active',show)});document.querySelectorAll('.nav-link').forEach(btn=>{const active=btn.dataset.view===name;btn.classList.toggle('active',active);if(active)btn.setAttribute('aria-current','page');else btn.removeAttribute('aria-current')});$('breadcrumb-current').textContent=({diagnose:'Overview',prioritize:'Opportunities',roi:'Value simulation',report:'Strategy brief'})[name];if(location.hash!==`#${name}`)history.replaceState(null,'',`#${name}`);if(scroll){document.querySelector(`#view-${name}`).scrollIntoView({behavior:'smooth',block:'start'})}}
function render(){const score=scoreReadiness();const cases=rankCases(score);$('metric-readiness').textContent=score.toFixed(1);$('metric-stage').textContent=band(score);$('metric-stage-note').textContent=score<35?'Build essential foundations':score<65?'Focus on operational readiness':'Candidate for selective scaling';$('metric-cases').textContent=String(cases.length).padStart(2,'0');$('metric-priority').textContent=cases[0].priority.toFixed(1);$('metric-priority-name').textContent=cases[0].name;const weak=[...DIMENSIONS].sort((a,b)=>state.ratings[a.key]-state.ratings[b.key]).slice(0,2).map(d=>d.short.toLowerCase());$('weakness-copy').textContent=`Strengthen ${weak[0]} and ${weak[1]} before scaling higher-risk use cases. Validate these self-reported scores with stakeholder evidence.`;renderRadar();renderOpportunities(cases);renderRoi();renderReport()}
function svgText(text,x,y,extra=''){return `<text x="${x}" y="${y}" ${extra}>${esc(text)}</text>`}
function renderRadar(){const cx=218,cy=169,r=113,steps=5,labels=DIMENSIONS.map(d=>d.axis);const at=(i,radius)=>{const angle=-Math.PI/2+i*2*Math.PI/5;return [cx+Math.cos(angle)*radius,cy+Math.sin(angle)*radius]};let s='';for(let k=1;k<=steps;k++){const pts=DIMENSIONS.map((d,i)=>at(i,r*k/steps).map(n=>n.toFixed(1)).join(',')).join(' ');s+=`<polygon points="${pts}" fill="${k%2?'#f8fbf8':'#f2f7f3'}" stroke="#dfe9e0" stroke-width="1" />`}
  DIMENSIONS.forEach((d,i)=>{const p=at(i,r);s+=`<line x1="${cx}" y1="${cy}" x2="${p[0]}" y2="${p[1]}" stroke="#dfe9e0" />`;const lab=at(i,r+29);let anchor='middle';if(lab[0]<cx-35)anchor='end';else if(lab[0]>cx+35)anchor='start';s+=svgText(labels[i],lab[0],lab[1]+4,`font-size="11" font-weight="600" text-anchor="${anchor}" fill="#667e70"`)});
  const polygon=DIMENSIONS.map((d,i)=>at(i,r*(state.ratings[d.key]-1)/4).map(n=>n.toFixed(1)).join(',')).join(' ');s+=`<polygon points="${polygon}" fill="#2d9670" fill-opacity=".20" stroke="#16816a" stroke-width="3" stroke-linejoin="round" />`;DIMENSIONS.forEach((d,i)=>{const p=at(i,r*(state.ratings[d.key]-1)/4);s+=`<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="#16816a" stroke="#fff" stroke-width="2" />`});$('radar-chart').innerHTML=s}
function renderOpportunities(cases){$('top-opportunities').innerHTML=cases.slice(0,3).map((c,i)=>`<article class="opportunity-card"><div class="opportunity-rank">0${i+1} / ${esc(c.category.toUpperCase())}</div><h3>${esc(c.name)}</h3><p>${esc(c.description)}</p><div class="opportunity-score"><strong>${c.priority.toFixed(1)}</strong><small>/ 100 PRIORITY</small></div><div class="priority-progress"><span style="width:${c.priority}%"></span></div><div class="opportunity-meta">${esc(c.risk)} risk · KPI: ${esc(c.kpi)}</div></article>`).join('');$('weight-list').innerHTML=weights.map(w=>`<div class="weight-item"><div class="weight-item-head"><span>${esc(w.name)}</span><span>${w.weight}%</span></div><div class="weight-track"><span style="width:${w.weight*2.8}%"></span></div></div>`).join('');$('governance-list').innerHTML=`<div class="governance-row head"><div>OPPORTUNITY</div><div>RISK</div><div>KEY GUARDRAIL</div><div>PILOT KPI</div></div>`+cases.slice(0,4).map(c=>`<div class="governance-row"><div class="name">${esc(c.name)}</div><div><span class="risk-label ${c.risk==='High'?'high':''}">${esc(c.risk)}</span></div><div>${esc(c.guardrail)}</div><div>${esc(c.kpi)}</div></div>`).join('');renderMatrix(cases);
  const sel=$('usecase');const current=state.selectedCase||cases[0].name;sel.innerHTML=cases.map(c=>`<option value="${esc(c.name)}">${esc(c.name)}</option>`).join('');sel.value=current;state.selectedCase=sel.value;
}
function renderMatrix(cases){const svg=$('matrix-chart');const xmin=1.3,xmax=5.25,ymin=2.25,ymax=5.3,w=700,h=390,L=65,R=28,T=30,B=56;const px=v=>L+(v-xmin)/(xmax-xmin)*(w-L-R),py=v=>h-B-(v-ymin)/(ymax-ymin)*(h-T-B);let out='';for(let j=2;j<=5;j++){const y=py(j);out+=`<line x1="${L}" y1="${y}" x2="${w-R}" y2="${y}" stroke="#e9efea"/>${svgText(j.toFixed(1),L-14,y+4,'font-size="11" text-anchor="end" fill="#9aaba2"')}`};for(let i=2;i<=5;i++){const x=px(i);out+=`<line x1="${x}" y1="${T}" x2="${x}" y2="${h-B}" stroke="#e9efea" />${svgText(i.toFixed(1),x,h-B+22,'font-size="11" text-anchor="middle" fill="#9aaba2"')}`};out+=svgText('IMPLEMENTATION EASE →',w/2,h-7,'font-size="11" text-anchor="middle" fill="#82978a" font-weight="700" letter-spacing="1"');out+=`<text x="15" y="${h/2}" transform="rotate(-90 15 ${h/2})" text-anchor="middle" font-size="11" fill="#82978a" font-weight="700" letter-spacing="1">BUSINESS IMPACT →</text>`;cases.forEach((c,i)=>{const x=px(c.ease),y=py(c.impact);const top=i===0;out+=`<circle cx="${x}" cy="${y}" r="${top?18:15}" fill="${top?'#198167':'#80ab9d'}" opacity=".88" stroke="#fff" stroke-width="3"><title>${esc(c.name)} | priority ${c.priority}/100 | impact ${c.impact}/5 | ease ${c.ease}/5</title></circle>`;out+=svgText(String(i+1),x,y+4,`text-anchor="middle" font-size="12" font-weight="800" fill="#fff"`)});svg.innerHTML=out; $('matrix-case-key').innerHTML=cases.map((c,i)=>`<span><b>${i+1}</b> ${esc(c.name)}</span>`).join('')}
function renderRoi(){const r=roiModel();$('result-hours').textContent=num(r.hours);$('result-gross').textContent=usd(r.gross);$('result-net').textContent=usd(r.firstYear);$('result-payback').textContent=r.payback===null?'Not reached':`${r.payback.toFixed(1)} mo`;$('result-roi').textContent=r.roi===null?'N/A':pct(r.roi);renderRoiChart(r.cumulative)}
function renderRoiChart(vals){const s=$('roi-chart'),width=590,height=260,left=77,right=29,top=24,bottom=45;let min=Math.min(...vals,0),max=Math.max(...vals,0);const pad=Math.max((max-min)*.15,5000);min-=pad;max+=pad;const x=i=>left+i*(width-left-right)/3;const y=v=>top+(max-v)/(max-min)*(height-top-bottom);let h='';for(let j=0;j<=4;j++){const v=min+(max-min)*j/4,yy=y(v);h+=`<line x1="${left}" y1="${yy}" x2="${width-right}" y2="${yy}" stroke="#e8efe9" />${svgText((v<0?'−':'')+'$'+Math.round(Math.abs(v)/1000)+'k',left-12,yy+3,'font-size="10" text-anchor="end" fill="#93a499"')}`}const zero=y(0);h+=`<line x1="${left}" y1="${zero}" x2="${width-right}" y2="${zero}" stroke="#b1c7b7" stroke-dasharray="5 4" />`;const pts=vals.map((v,i)=>`${x(i)},${y(v)}`).join(' ');const area=`${x(0)},${zero} ${pts} ${x(3)},${zero}`;h+=`<polygon points="${area}" fill="#dff1e5" fill-opacity=".8" /><polyline points="${pts}" fill="none" stroke="#178066" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />`;vals.forEach((v,i)=>{h+=`<circle cx="${x(i)}" cy="${y(v)}" r="5.3" fill="#168167" stroke="#fff" stroke-width="2"><title>${['Initial','Year 1','Year 2','Year 3'][i]}: ${usd(v)}</title></circle>`;h+=svgText(['Initial','Year 1','Year 2','Year 3'][i],x(i),height-12,'font-size="11" text-anchor="middle" fill="#82968a"')});s.innerHTML=h}
function modelData(){return {score:scoreReadiness(),cases:rankCases(scoreReadiness()),r:roiModel()}}
function renderReport(){const {score,cases,r}=modelData();const top=cases.slice(0,3),stage=band(score),date=new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}),company=esc(state.company);const cash=r.roi===null?'N/A':pct(r.roi),payback=r.payback===null?'Not reached':r.payback.toFixed(1)+' months';$('report-content').innerHTML=`<div class="report-head"><div><div class="report-overline">ATN / EXECUTIVE BRIEF</div><h3>Enterprise AI transformation</h3><p>Opportunity assessment & prioritized pilot strategy</p></div><div class="report-date">PREPARED<br>${esc(date)}<br>DEMO / INTERNAL</div></div>
  <div class="report-meta"><div><span>CLIENT</span><strong>${company}</strong></div><div><span>SECTOR</span><strong>${esc(state.sector)}</strong></div><div><span>EMPLOYEES</span><strong>${num(state.employees)}</strong></div></div>
  <div class="report-section"><h4><em>01</em> Executive summary</h4><p>Based on five self-assessed dimensions, the organization receives a readiness score of <strong>${score.toFixed(1)}/100 (${stage})</strong>. The most attractive current pilot hypothesis is <strong>${esc(top[0].name)}</strong>, with a heuristic priority score of ${top[0].priority.toFixed(1)}/100. Conduct a limited discovery phase to test technical feasibility, process ownership and governance requirements before committing to a scaled deployment.</p></div>
  <div class="report-section"><h4><em>02</em> Top three opportunities</h4><div class="report-points">${top.map((c,i)=>`<div class="report-point"><span>0${i+1} / ${c.priority.toFixed(1)} PRIORITY</span><strong>${esc(c.name)}</strong><p>${esc(c.kpi)}<br>${esc(c.risk)} risk</p></div>`).join('')}</div><p>Priority weights: business impact 35%, implementation ease 30%, sector fit 20%, readiness fit 15%. Case ratings are expert-style illustrative assumptions.</p></div>
  <div class="report-section"><h4><em>03</em> Indicative business case</h4><table class="report-table"><tbody>
    <tr><td>Use case</td><td>${esc(state.selectedCase||top[0].name)}</td></tr>
    <tr><td>Employees in pilot / effective adoption</td><td>${num(state.roi.affected)} / ${state.roi.adoption}%</td></tr>
    <tr><td>Annual hours released</td><td>${num(r.hours)} h</td></tr>
    <tr><td>Gross capacity value / year</td><td>${usd(r.gross)}</td></tr>
    <tr><td>One-time / annual recurring investment</td><td>${usd(state.roi.upfront)} / ${usd(state.roi.recurring)}</td></tr>
    <tr><td>First-year net capacity value</td><td>${usd(r.firstYear)}</td></tr>
    <tr><td>Indicative first-year ROI / simple payback</td><td>${cash} / ${payback}</td></tr>
  </tbody></table></div>
  <div class="report-section"><h4><em>04</em> Suggested 90-day pilot plan</h4><div class="roadmap"><div><span>DAYS 01—30</span><strong>Discover</strong><p>Map workflows, secure data permissions, establish baseline KPIs and involve users.</p></div><div><span>DAYS 31—60</span><strong>Validate</strong><p>Prototype a narrow use case and test accuracy, exception handling and adoption.</p></div><div><span>DAYS 61—90</span><strong>Decide</strong><p>Evaluate governance controls, quantify actual benefit and set scale / stop criteria.</p></div></div></div>
  <p class="report-disclaimer">Methodology note: Fictional scenario and self-assessed heuristic ratings, not a validated industry benchmark. Labor-capacity value does not necessarily represent realized cash savings. No personal or company data is sent to a server. Independent portfolio project; not affiliated with Deloitte.</p>`}
function markdownReport(){const {score,cases,r}=modelData(),top=cases.slice(0,3);const clean=s=>String(s).replace(/[\r\n]/g,' ').replace(/([*_`\[\]#])/g,'\\$1');const cell=(k,v)=>`| ${k} | ${v} |`;const report=[
  '# AI TRANSFORMATION NAVIGATOR',
  '## Illustrative executive strategy brief','',
  `**Company:** ${clean(state.company)}`,
  `**Sector:** ${clean(state.sector)}`,
  `**Employees:** ${state.employees.toLocaleString('en-US')}`,
  `**Readiness:** ${score.toFixed(1)}/100 (${band(score)})`,'',
  '### 1. Readiness assessment','',
  ...DIMENSIONS.map(d=>`- ${d.key}: ${state.ratings[d.key]}/5 (weight ${d.weight*100}%)`),'',
  'Readiness = Σ [(rating − 1) / 4 × weight × 100]. Self-assessed heuristic, not a validated benchmark.','',
  '### 2. Prioritized use cases','',
  ...top.flatMap((c,i)=>[`${i+1}. **${c.name}** — Priority ${c.priority.toFixed(1)}/100; ${c.risk.toLowerCase()} risk.`, `   - Scope: ${c.description}`,`   - Pilot KPI: ${c.kpi}`,`   - Guardrail: ${c.guardrail}`]),'',
  'Priority model: 35% business impact, 30% ease, 20% sector fit, 15% readiness fit. Scores are illustrative.','',
  '### 3. Financial scenario (USD)','',
  '| Measure | Value |','|---|---:|',
  cell('Pilot use case',clean(state.selectedCase||top[0].name)),
  cell('Employees affected',num(state.roi.affected)),
  cell('Hours saved per week',state.roi.hours),
  cell('Adoption rate',state.roi.adoption+'%'),
  cell('Loaded hourly cost',usd(state.roi.cost)),
  cell('Working weeks',state.roi.weeks),
  cell('One-time cost',usd(state.roi.upfront)),
  cell('Recurring annual cost',usd(state.roi.recurring)),
  cell('Annual hours released',num(r.hours)),
  cell('Gross annual capacity value',usd(r.gross)),
  cell('First-year net capacity value',usd(r.firstYear)),
  cell('First-year ROI',r.roi===null?'N/A':pct(r.roi)),
  cell('Simple payback',r.payback===null?'Not reached':r.payback.toFixed(1)+' months'),'',
  '**Caution:** Employee capacity released is not the same as booked cash savings. Realized benefits depend on implementation, adoption, redeployment and observed outcomes.','',
  '### 4. Suggested 90-day pilot roadmap','',
  '- **Days 1–30 — Discover:** Map process, involve stakeholders, establish baseline KPI, assess governance and data access.',
  '- **Days 31–60 — Validate:** Prototype a narrow use case, evaluate accuracy and human review, test end-user uptake.',
  '- **Days 61–90 — Decide:** Measure actual results, estimate realized economics and apply predefined scale / stop criteria.','',
  '### Disclosure','',
  'Independent educational portfolio project. Not affiliated with Deloitte or any consulting firm. Scenario ratings are hypothetical. No large-language-model API is called; all calculations run locally in the browser.'
];return report.join('\n')+'\n'}
function downloadMarkdown(){const blob=new Blob([markdownReport()],{type:'text/markdown;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);const short=state.company.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,35)||'client';a.download=`${short}-ai-strategy-brief.md`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function init(){const year=new Date().getFullYear();$('today').textContent=year;$('copyright-year').textContent=year;setupControls();$('affected').max=state.employees;$('adoption').style.setProperty('--fill','60%');render();const hash=location.hash.replace('#','');activate(['diagnose','prioritize','roi','report'].includes(hash)?hash:'diagnose',false)}
document.addEventListener('DOMContentLoaded',init);
