(() => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const scoreEl = document.getElementById("score");
  const statusEl = document.getElementById("status");
  const W = canvas.width, H = canvas.height;
  const keys = {left:false,right:false,jump:false};
  const platforms = [
    {x:0,y:486,w:960,h:54},{x:145,y:390,w:170,h:18},{x:390,y:320,w:160,h:18},
    {x:650,y:390,w:160,h:18},{x:760,y:260,w:130,h:18}
  ];
  const gemsStart = [{x:205,y:350},{x:455,y:280},{x:710,y:350},{x:810,y:220},{x:565,y:445}];
  let player, gems, slimes, score, state, last=0, cameraTick=0;

  function reset(){
    player={x:48,y:430,w:28,h:38,vx:0,vy:0,onGround:false,face:1,invuln:0};
    gems=gemsStart.map(g=>({...g,taken:false}));
    slimes=[{x:330,y:460,w:30,h:24,min:320,max:380,dir:1,speed:1.15},{x:570,y:460,w:30,h:24,min:550,max:625,dir:-1,speed:1.35},{x:690,y:364,w:30,h:24,min:660,max:780,dir:1,speed:1}];
    score=0;state="playing";scoreEl.textContent="0 / 5";statusEl.textContent="Collect all 5 gems. Avoid the slimes!";
  }
  function rect(x,y,w,h,color){ctx.fillStyle=color;ctx.fillRect(Math.round(x),Math.round(y),w,h)}
  function drawBackground(){
    rect(0,0,W,H,"#83c9d3");
    // distant blocky hills
    for(let i=0;i<8;i++){const x=i*150-(cameraTick%150);rect(x,270,100,220,"#75b98e");rect(x+25,245,55,25,"#75b98e");rect(x+48,225,25,20,"#75b98e")}
    // clouds
    for(let i=0;i<4;i++){const x=(i*280+80-cameraTick*.25)%(W+100)-50;rect(x,75,58,14,"#dff5e8");rect(x+12,61,30,14,"#dff5e8");}
    rect(0,486,W,54,"#315c45");rect(0,486,W,7,"#9bd477");
    for(let x=8;x<W;x+=32){rect(x,505,3,3,"#477b53");rect(x+12,525,4,3,"#477b53")}
  }
  function drawPlatforms(){for(const p of platforms.slice(1)){rect(p.x,p.y,p.w,p.h,"#6b4938");rect(p.x,p.y,p.w,5,"#b5dc78");for(let x=p.x+8;x<p.x+p.w-5;x+=22)rect(x,p.y+9,7,4,"#80583f")}}
  function drawGem(g){if(g.taken)return;const bob=Math.sin(Date.now()/170+g.x)*3;ctx.save();ctx.translate(g.x,g.y+bob);ctx.fillStyle="#ffe36e";ctx.beginPath();ctx.moveTo(0,-12);ctx.lineTo(10,0);ctx.lineTo(0,12);ctx.lineTo(-10,0);ctx.closePath();ctx.fill();rect(-2,-7,3,9,"#fff5b0");ctx.restore()}
  function drawPlayer(){const p=player;ctx.save();if(p.invuln>0&&Math.floor(Date.now()/80)%2===0)ctx.globalAlpha=.4;
    // tiny adventurer
    rect(p.x+6,p.y,16,9,"#26374d");rect(p.x+4,p.y+7,20,13,"#f2bd78");rect(p.x+2,p.y+18,24,15,"#e45c48");
    rect(p.x+8,p.y+10,3,3,"#18232b");rect(p.x+19,p.y+10,3,3,"#18232b");rect(p.x+8,p.y+32,6,6,"#35445a");rect(p.x+18,p.y+32,6,6,"#35445a");
    rect(p.x+(p.face>0?24:0),p.y+20,5,5,"#f2bd78");ctx.restore()}
  function drawSlime(s){rect(s.x,s.y+8,s.w,s.h-8,"#4caa70");rect(s.x+5,s.y,s.w-10,9,"#70d68a");rect(s.x+7,s.y+12,4,5,"#10251e");rect(s.x+20,s.y+12,4,5,"#10251e");rect(s.x+11,s.y+20,9,2,"#194b37")}
  function overlap(a,b){return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y}
  function update(dt){
    if(state!=="playing")return;
    const p=player,step=Math.min(dt/16.67,2.2);
    p.vx=(keys.right?3.1:0)-(keys.left?3.1:0);if(p.vx)p.face=Math.sign(p.vx);
    if(keys.jump&&p.onGround){p.vy=-10.8;p.onGround=false}
    p.vy=Math.min(p.vy+.48*step,12);p.x+=p.vx*step;p.y+=p.vy*step;p.x=Math.max(0,Math.min(W-p.w,p.x));p.onGround=false;
    for(const plat of platforms){if(p.vy>=0&&p.x+p.w>plat.x&&p.x<plat.x+plat.w&&p.y+p.h>=plat.y&&p.y+p.h-p.vy*step<=plat.y){p.y=plat.y-p.h;p.vy=0;p.onGround=true}}
    for(const s of slimes){s.x+=s.dir*s.speed*step;if(s.x<s.min||s.x+s.w>s.max){s.dir*=-1;s.x=Math.max(s.min,Math.min(s.max-s.w,s.x))}if(overlap(p,s)&&p.invuln<=0){state="lost";statusEl.textContent="A slime got you! Press RESTART to try again.";}}
    for(const g of gems){if(!g.taken&&overlap(p,{x:g.x-9,y:g.y-10,w:18,h:20})){g.taken=true;score++;scoreEl.textContent=score+" / 5";if(score===5){state="won";statusEl.textContent="You found every gem. Quest complete! 🎉"}}}
    if(p.y>H){state="lost";statusEl.textContent="You fell! Press RESTART to try again."}
    if(p.invuln>0)p.invuln-=dt;
    cameraTick+=.12*step;
  }
  function draw(){
    drawBackground();drawPlatforms();gems.forEach(drawGem);slimes.forEach(drawSlime);drawPlayer();
    if(state!=="playing"){ctx.fillStyle="rgba(12,22,28,.72)";ctx.fillRect(0,0,W,H);ctx.fillStyle="#fff";ctx.textAlign="center";ctx.font="bold 34px monospace";ctx.fillText(state==="won"?"LEVEL COMPLETE!":"GAME OVER",W/2,H/2);ctx.font="16px monospace";ctx.fillText("Press RESTART to play again",W/2,H/2+34)}
  }
  function loop(t){const dt=t-last||16.67;last=t;update(dt);draw();requestAnimationFrame(loop)}
  function setKey(name,value){keys[name]=value}
  window.addEventListener("keydown",e=>{if(["ArrowLeft","ArrowRight","ArrowUp"," ","a","A","d","D","w","W"].includes(e.key))e.preventDefault();if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")setKey("left",true);if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")setKey("right",true);if(e.key===" "||e.key==="ArrowUp"||e.key==="w"||e.key==="W")setKey("jump",true)});
  window.addEventListener("keyup",e=>{if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")setKey("left",false);if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")setKey("right",false);if(e.key===" "||e.key==="ArrowUp"||e.key==="w"||e.key==="W")setKey("jump",false)});
  document.querySelectorAll("[data-key]").forEach(btn=>{const k=btn.dataset.key;btn.addEventListener("pointerdown",e=>{e.preventDefault();setKey(k,true)});["pointerup","pointerleave","pointercancel"].forEach(ev=>btn.addEventListener(ev,()=>setKey(k,false)))});
  document.getElementById("restart").addEventListener("click",reset);
  reset();requestAnimationFrame(loop);
})();