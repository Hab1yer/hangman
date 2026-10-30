const $=id=>document.getElementById(id); let state=null,busy=false;
for(const letter of 'abcdefghijklmnopqrstuvwxyz'){const b=document.createElement('button');b.textContent=letter.toUpperCase();b.onclick=()=>guess(letter);$('keyboard').append(b);}
function render(){
 $('new').disabled=busy;
 [...$('keyboard').children].forEach(b=>{const l=b.textContent.toLowerCase();b.disabled=busy||!state||state.status!=='playing'||state.guessed_letters.includes(l);b.className=state?.guessed_letters.includes(l)?state.incorrect_letters.includes(l)?'incorrect':'correct':'';});
 if(!state)return;
 $('pattern').textContent=state.pattern.toUpperCase();$('remaining').textContent=state.remaining_guesses;
 $('wrong').textContent='Incorrect letters: '+(state.incorrect_letters.join(', ').toUpperCase()||'—');
 [...$('figure').children].forEach((p,i)=>p.style.visibility=i<6-state.remaining_guesses?'visible':'hidden');
 $('status').textContent=state.status==='playing'?'Find the word.':state.status==='won'?`You won! ${state.word.toUpperCase()}.`:`The word was ${state.word.toUpperCase()}. Try again?`;
}
async function send(url,data){busy=true;render();try{const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const result=await r.json();if(!r.ok)throw Error(result.error);state=result;busy=false;render();}catch(e){busy=false;render();$('status').textContent=e.message+' Please try again.';}}
function guess(letter){if(!busy&&state&&state.status==='playing'&&!state.guessed_letters.includes(letter))send(`/api/games/${state.game_id}/guess`,{letter});}
$('new').onclick=()=>{if(!busy)send('/api/games',{difficulty:$('difficulty').value});};
document.addEventListener('keydown', e => {
 if (e.ctrlKey || e.metaKey || e.altKey || e.repeat) return;
 if (e.target.isContentEditable || ['SELECT', 'INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
 if (/^[a-z]$/i.test(e.key)) {
  e.preventDefault();
  guess(e.key.toLowerCase());
 }
});
render();$('new').click();
