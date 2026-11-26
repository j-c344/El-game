const data=[
 {id:"snake",title:"Neon Snake",cat:"Arcade",emoji:"🐍",desc:"Attrape les points et grandis.",bg:"linear-gradient(135deg,#123b3b,#1b806d)"},
 {id:"memory",title:"Memory Match",cat:"Puzzle",emoji:"🧠",desc:"Retrouve les paires cachées.",bg:"linear-gradient(135deg,#43265f,#9b5bd4)"},
 {id:"clicker",title:"Space Clicker",cat:"Arcade",emoji:"🚀",desc:"Clique pour gagner des étoiles.",bg:"linear-gradient(135deg,#202d61,#536de2)"},
 {id:"pong",title:"Pocket Pong",cat:"Sport",emoji:"🏓",desc:"Renvoie la balle et marque.",bg:"linear-gradient(135deg,#60321c,#e58b42)"}
];
let lang="fr",category="Tous";
const cats=["Tous","Arcade","Puzzle","Sport"];
const $=id=>document.getElementById(id);
const SUPABASE_URL="https://xlfbnulmyfoigrpgbzly.supabase.co";
// Publishable keys are intended for browser use. Never put a Supabase secret/service-role key here.
const SUPABASE_PUBLISHABLE_KEY="sb_publishable_mJ_6TwJbmHB_h7ozTAykXA_k6VBIl2o";
const SCORE_API=`${SUPABASE_URL}/rest/v1/scores`;
let selectedLeaderboard="snake";
function tr(fr,en){return lang==="fr"?fr:en}
function renderCats(){$("categories").innerHTML=cats.map(c=>`<button class="cat ${category===c?"active":""}" data-cat="${c}">${c==="Tous"?tr("Tous","All"):c}</button>`).join("");document.querySelectorAll(".cat").forEach(b=>b.onclick=()=>{category=b.dataset.cat;renderCats();render()})}
function render(){let q=$("search").value.toLowerCase();let list=data.filter(g=>(category==="Tous"||g.cat===category)&&(g.title.toLowerCase().includes(q)||g.desc.toLowerCase().includes(q)||g.cat.toLowerCase().includes(q)));$("count").textContent=tr(`${list.length} jeux`,`${list.length} games`);$("empty").hidden=!!list.length;$("games").innerHTML=list.map(g=>`<article class="card" data-id="${g.id}"><div class="thumb" style="background:${g.bg}">${g.emoji}</div><div class="cardinfo"><h3>${g.title}</h3><p>${g.desc}</p><span class="tag">${g.cat}</span></div></article>`).join("");document.querySelectorAll(".card").forEach(c=>c.onclick=()=>play(c.dataset.id))}
function installLeaderboard(){
 const style=document.createElement("style");
 style.textContent=`.leaderboard{max-width:1100px;margin:40px auto 55px;padding:24px;background:var(--panel);border:1px solid #25283a;border-radius:18px}.leaderboard h2{margin:0 0 8px;font-family:'Space Grotesk',sans-serif}.leaderboard p{color:var(--muted)}.lb-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:18px 0}.lb-controls input,.lb-controls select{background:#0c0d14;color:var(--text);border:1px solid #34374c;border-radius:9px;padding:11px 13px;font:inherit}.lb-controls input{min-width:190px}.lb-controls button{border:0;border-radius:9px;padding:11px 16px;background:var(--purple);color:white;font:inherit;font-weight:700;cursor:pointer}.lb-status{min-height:1.4em;margin:8px 0;color:var(--muted)}.lb-list{padding:0;margin:0;list-style:none}.lb-list li{display:flex;justify-content:space-between;gap:16px;padding:11px 4px;border-bottom:1px solid #292c3d}.lb-list li:last-child{border-bottom:0}.lb-rank{color:var(--purple);font-weight:800;min-width:32px}.lb-player{flex:1;overflow-wrap:anywhere}.lb-score{font-weight:800}.lb-empty{color:var(--muted);padding:14px 0}`;
 document.head.appendChild(style);
 const section=document.createElement("section");section.className="leaderboard";section.id="leaderboard";section.innerHTML=`<p class="eyebrow" data-fr="LES MEILLEURS JOUEURS" data-en="TOP PLAYERS">LES MEILLEURS JOUEURS</p><h2 data-fr="Classement" data-en="Leaderboard">Classement</h2><p data-fr="Un classement indépendant pour chaque jeu." data-en="A separate leaderboard for every game.">Un classement indépendant pour chaque jeu.</p><div class="lb-controls"><label for="lb-game">${tr("Jeu","Game")}</label><select id="lb-game">${data.map(g=>`<option value="${g.id}">${g.title}</option>`).join("")}</select><label for="lb-name">${tr("Pseudo","Nickname")}</label><input id="lb-name" type="text" maxlength="20" autocomplete="nickname" placeholder="${tr("Ton pseudo","Your nickname")}"><button id="lb-save-name" type="button">${tr("Enregistrer","Save")}</button><button id="lb-refresh" type="button">↻</button></div><p id="lb-status" class="lb-status" role="status" aria-live="polite"></p><ol id="lb-list" class="lb-list"></ol>`;
 const main=document.querySelector("main");main.insertAdjacentElement("afterend",section);
 const nameInput=$("lb-name");nameInput.value=localStorage.getItem("el-game-nickname")||"";
 $("lb-game").onchange=()=>{selectedLeaderboard=$("lb-game").value;loadLeaderboard()};
 $("lb-refresh").onclick=loadLeaderboard;
 $("lb-save-name").onclick=()=>saveNickname(true);
 nameInput.addEventListener("keydown",e=>{if(e.key==="Enter")saveNickname(true)});
 loadLeaderboard();
}
function saveNickname(showStatus=false){
 const input=$("lb-name"),name=input.value.trim();
 if(!/^[\\p{L}\\p{N}_ -]{2,20}$/u.test(name)){if(showStatus)$("lb-status").textContent=tr("Choisis un pseudo de 2 à 20 caractères (lettres, chiffres, espaces, _ ou -).","Choose a 2–20 character nickname (letters, numbers, spaces, _ or -).");return null}
 localStorage.setItem("el-game-nickname",name);input.value=name;
 if(showStatus)$("lb-status").textContent=tr("Pseudo enregistré sur cet appareil.","Nickname saved on this device.");
 return name;
}
function headers(){return {"apikey":SUPABASE_PUBLISHABLE_KEY,"Authorization":`Bearer ${SUPABASE_PUBLISHABLE_KEY}`,"Content-Type":"application/json"}}
async function loadLeaderboard(){
 const list=$("lb-list"),status=$("lb-status");if(!list||!status)return;
 selectedLeaderboard=$("lb-game").value||selectedLeaderboard;
 status.textContent=tr("Chargement…","Loading…");list.innerHTML="";
 try{
  const url=`${SCORE_API}?select=player_name,score&game_id=eq.${encodeURIComponent(selectedLeaderboard)}&order=score.desc&limit=10`;
  const response=await fetch(url,{headers:headers()});if(!response.ok)throw new Error(await response.text());
  const rows=await response.json();
  if(!rows.length){list.innerHTML=`<li class="lb-empty">${tr("Pas encore de score. Lance une partie !","No scores yet. Start a game!")}</li>`}
  else list.innerHTML=rows.map((row,index)=>`<li><span class="lb-rank">${index+1}.</span><span class="lb-player">${escapeHtml(row.player_name)}</span><span class="lb-score">${Number(row.score).toLocaleString(lang==="fr"?"fr-FR":"en-US")}</span></li>`).join("");
  status.textContent="";
 }catch(error){status.textContent=tr("Classement indisponible. Vérifie la configuration Supabase et le script SQL dans README.txt.","Leaderboard unavailable. Check the Supabase setup and SQL script in README.txt.");console.error("Supabase leaderboard load failed:",error)}
}
function escapeHtml(value){const node=document.createElement("span");node.textContent=String(value);return node.innerHTML}
async function submitScore(gameId,score){
 if(!data.some(game=>game.id===gameId)||!Number.isSafeInteger(score)||score<0||score>1000000000)return;
 const playerName=saveNickname();
 if(!playerName){$("lb-status").textContent=tr("Saisis d’abord un pseudo valide dans le classement.","Enter a valid nickname in the leaderboard first.");return}
 try{
  const response=await fetch(`${SCORE_API}?on_conflict=game_id,player_name`,{method:"POST",headers:{...headers(),"Prefer":"resolution=merge-duplicates,return=minimal"},body:JSON.stringify({game_id:gameId,player_name:playerName,score})});
  if(!response.ok)throw new Error(await response.text());
  selectedLeaderboard=gameId;$("lb-game").value=gameId;
  $("lb-status").textContent=tr(`Score ${score} enregistré pour ${playerName} !`,`Score ${score} saved for ${playerName}!`);
  await loadLeaderboard();
 }catch(error){$("lb-status").textContent=tr("Enregistrement impossible. Vérifie la configuration Supabase.","Could not save score. Check the Supabase setup.");console.error("Supabase score submission failed:",error)}
}
function play(id){let g=data.find(x=>x.id===id);selectedLeaderboard=id;$("lb-game").value=id;$("playingTitle").textContent=g.title;$("frame").src=`${id}.html`;$("player").hidden=false;document.body.style.overflow="hidden"}
function close(){$("frame").src="about:blank";$("player").hidden=true;document.body.style.overflow=""}
$("back").onclick=close;$("fullscreen").onclick=()=>{let f=$("frame");if(f.requestFullscreen)f.requestFullscreen()};$("search").oninput=render;
window.addEventListener("message",event=>{if(event.source!==$("frame").contentWindow)return;const message=event.data;if(!message||message.type!=="el-game-score")return;submitScore(message.game,message.score)});
$("lang").onclick=()=>{lang=lang==="fr"?"en":"fr";$("lang").textContent=lang==="fr"?"EN":"FR";document.documentElement.lang=lang;document.querySelectorAll("[data-fr]").forEach(e=>{let val=e.dataset[lang];if(val)e.innerHTML=val});$("search").placeholder=tr("Rechercher un jeu...","Search games...");category="Tous";renderCats();render();const savedName=localStorage.getItem("el-game-nickname");if($("lb-name"))$("lb-name").value=savedName||"";if($("lb-game"))loadLeaderboard()};
installLeaderboard();renderCats();render();