const data=[
{id:"snake",title:"Neon Snake",cat:"Arcade",emoji:"🐍",desc:"Attrape les points et grandis.",bg:"linear-gradient(135deg,#123b3b,#1b806d)"},
{id:"memory",title:"Memory Match",cat:"Puzzle",emoji:"🧠",desc:"Retrouve les paires cachées.",bg:"linear-gradient(135deg,#43265f,#9b5bd4)"},
{id:"clicker",title:"Space Clicker",cat:"Arcade",emoji:"🚀",desc:"Clique pour gagner des étoiles.",bg:"linear-gradient(135deg,#202d61,#536de2)"},
{id:"pong",title:"Pocket Pong",cat:"Sport",emoji:"🏓",desc:"Renvoie la balle et marque.",bg:"linear-gradient(135deg,#60321c,#e58b42)"}];
let lang="fr",category="Tous";
const cats=["Tous","Arcade","Puzzle","Sport"];
const $=id=>document.getElementById(id);
function tr(fr,en){return lang==="fr"?fr:en}
function renderCats(){$("categories").innerHTML=cats.map(c=>`<button class="cat ${category===c?"active":""}" data-cat="${c}">${c==="Tous"?tr("Tous","All"):c}</button>`).join("");document.querySelectorAll(".cat").forEach(b=>b.onclick=()=>{category=b.dataset.cat;renderCats();render()})}
function render(){let q=$("search").value.toLowerCase();let list=data.filter(g=>(category==="Tous"||g.cat===category)&&(g.title.toLowerCase().includes(q)||g.desc.toLowerCase().includes(q)||g.cat.toLowerCase().includes(q)));$("count").textContent=tr(`${list.length} jeux`,` ${list.length} games`);$("empty").hidden=!!list.length;$("games").innerHTML=list.map(g=>`<article class="card" data-id="${g.id}"><div class="thumb" style="background:${g.bg}">${g.emoji}</div><div class="cardinfo"><h3>${g.title}</h3><p>${g.desc}</p><span class="tag">${g.cat}</span></div></article>`).join("");document.querySelectorAll(".card").forEach(c=>c.onclick=()=>play(c.dataset.id))}
function play(id){let g=data.find(x=>x.id===id);$("playingTitle").textContent=g.title;$("frame").src=`${id}.html`;$("player").hidden=false;document.body.style.overflow="hidden"}
function close(){ $("frame").src="about:blank";$("player").hidden=true;document.body.style.overflow=""}
$("back").onclick=close;$("fullscreen").onclick=()=>{let f=$("frame");if(f.requestFullscreen)f.requestFullscreen()};$("search").oninput=render;
$("lang").onclick=()=>{lang=lang==="fr"?"en":"fr";$("lang").textContent=lang==="fr"?"EN":"FR";document.documentElement.lang=lang;document.querySelectorAll("[data-fr]").forEach(e=>{let val=e.dataset[lang];if(val)e.innerHTML=val});$("search").placeholder=tr("Rechercher un jeu...","Search games...");category="Tous";renderCats();render()};
renderCats();render();