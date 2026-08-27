/*
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

Unauthorized copying, redistribution, republication, or commercial use of
original NMS Tech material is prohibited without prior written authorization.
Third-party components remain subject to their own licences.
*/

const form=document.getElementById("patientForm");
const result=document.getElementById("result");

form.addEventListener("submit",async(e)=>{
 e.preventDefault();
 result.classList.remove("hidden");
 result.innerHTML="<h2>Analyzing…</h2><p>Running safety checks, differential engine and local LLM.</p>";
 const fd=new FormData(form), p={};
 for(const [k,v] of fd.entries()) p[k]=v;
 if(p.age)p.age=Number(p.age);
 try{
  const res=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({patient:p,question:p.question||""})});
  const data=await res.json();
  let html="<h2>Clinical Analysis</h2>";
  if(data.emergency_flags.length)html+=`<div class="card danger"><h3>Safety alerts</h3>${data.emergency_flags.map(x=>`<p>⚠️ ${escapeHtml(x)}</p>`).join("")}</div>`;
  html+=`<div class="card"><h3>Differential</h3>${data.differential.map(d=>`<p><strong>${escapeHtml(d.diagnosis)}</strong> — ${escapeHtml(d.priority)}<br>${escapeHtml(d.supporting)}</p>`).join("")}</div>`;
  html+=`<div class="card"><h3>Suggested evaluation</h3>${data.suggested_evaluation.map(x=>`<p>• ${escapeHtml(x)}</p>`).join("")}</div>`;
  html+=`<div class="card"><h3>AI response</h3><div>${escapeHtml(data.answer).replaceAll("\n","<br>")}</div></div>`;
  html+=`<div class="card"><h3>References</h3>${data.citations.map(c=>`<p class="citation"><strong>${escapeHtml(c.id)}</strong> — ${escapeHtml(c.title)} — ${escapeHtml(c.organization)}<br><a href="${encodeURI(c.url)}" target="_blank" rel="noopener">${escapeHtml(c.url)}</a><br>${escapeHtml(c.note)}</p>`).join("")}</div>`;
  html+=`<p><strong>${escapeHtml(data.disclaimer)}</strong></p>`;
  result.innerHTML=html;
 }catch(err){result.innerHTML=`<h2>Error</h2><p>${escapeHtml(String(err))}</p>`;}
});
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}
