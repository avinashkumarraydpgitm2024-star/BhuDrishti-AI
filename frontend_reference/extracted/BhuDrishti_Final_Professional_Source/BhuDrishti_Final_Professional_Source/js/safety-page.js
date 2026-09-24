document.addEventListener('DOMContentLoaded',()=>{
  const data=window.BHUDRISHTI_RISK_DATA||[];
  const search=document.getElementById('riskSearch');
  const list=document.getElementById('riskLocations');
  const feedback=document.getElementById('riskSearchFeedback');
  data.forEach(x=>{const o=document.createElement('option');o.value=x['Location Name'];list.appendChild(o)});
  let current=null;

  function clearFeedback(){if(feedback) feedback.textContent=''}
  function render(item){
    if(!item)return;
    clearFeedback();
    current=item;
    localStorage.setItem('bhudrishtiSelectedRiskLocation',item['Location Name']);
    BhuApp.setArea(item['Location Name']+', Sikkim');
    search.value=item['Location Name'];
    const loc=BhuApp.localizedRisk(item),score=item['Risk Score']||80,level=item['Risk Level']||'High';
    document.getElementById('riskScore').textContent=score;
    const ring=document.getElementById('riskRing');
    ring.style.setProperty('--score',score);
    ring.style.setProperty('--ring',level==='High'?'var(--danger)':level==='Medium'?'var(--warn)':'var(--safe)');
    document.getElementById('riskLocation').textContent=item['Location Name'];
    document.getElementById('riskDistrict').textContent=String(item['District']||'').replace(' (source classification)','');
    document.getElementById('riskType').textContent=BhuApp.localizeRiskType(item['Risk Type']);
    document.getElementById('riskReason').textContent=loc.reason;
    document.getElementById('recoveryText').textContent=loc.recovery;
    document.getElementById('routeText').textContent=loc.route;
    document.getElementById('sourceDoc').textContent=loc.source;
    document.getElementById('sourceNote').textContent=loc.note;
    document.getElementById('sourceLink').href=item['Official Source Page'];
    const chip=document.getElementById('riskChip');
    chip.textContent=BhuApp.localizeLevel(level)+' '+BhuApp.t('risk');
    chip.className='status-chip '+(level==='High'?'chip-high':level==='Medium'?'chip-medium':'chip-low');
    const wl=document.getElementById('warningList'),sl=document.getElementById('safetyList');
    wl.innerHTML='';sl.innerHTML='';
    loc.warnings.forEach(v=>{const li=document.createElement('li');li.textContent=v;wl.appendChild(li)});
    loc.safety.forEach(v=>{const li=document.createElement('li');li.textContent=v;sl.appendChild(li)});
  }

  function find(value=search.value){
    const q=String(value||'').trim().toLowerCase();
    if(!q)return null;
    return data.find(x=>x['Location Name'].toLowerCase()===q)||data.find(x=>x['Location Name'].toLowerCase().includes(q));
  }
  function submit(){
    const item=find();
    if(item){render(item);return}
    if(feedback) feedback.textContent=BhuApp.t('locationNotFound');
    search.focus();
  }

  document.getElementById('riskCheck').addEventListener('click',submit);
  search.addEventListener('keydown',e=>{if(e.key==='Enter')submit()});
  search.addEventListener('input',clearFeedback);
  document.querySelectorAll('[data-risk-location]').forEach(btn=>btn.addEventListener('click',()=>{
    const item=find(btn.dataset.riskLocation);if(item)render(item);
  }));
  document.addEventListener('app:language',()=>{if(current)render(current);else clearFeedback()});
  const saved=localStorage.getItem('bhudrishtiSelectedRiskLocation');
  render(data.find(x=>x['Location Name']===saved)||data[0]);
});
