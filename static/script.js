let gaugeChart;

function startCam(){
fetch('/start',{method:'POST'});
document.getElementById('status').innerText='Running';
}

function stopCam(){
fetch('/stop',{method:'POST'});
document.getElementById('status').innerText='Stopped';
}

function loadWeek(){
fetch('/week').then(r=>r.json()).then(d=>{
let html='';
for(let day in d){
html += `<div class="day"><b>${day}</b><br>`;
html += d[day].length ? d[day].join(", ") : "No student";
html += `</div>`;
}
document.getElementById('week').innerHTML = html;
});
}

function rate(v){
fetch('/rate',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({rating:v})
});
alert("Thanks for feedback");
}

function loadGauge(){
fetch('/feedback_avg').then(r=>r.json()).then(data=>{
const avg = data.avg;
document.getElementById("avgText").innerText = avg;

const ctx = document.getElementById("gauge").getContext("2d");
if(gaugeChart) gaugeChart.destroy();

gaugeChart = new Chart(ctx,{
type:'doughnut',
data:{datasets:[{data:[avg,5-avg],backgroundColor:['#4CAF50','#ddd'],borderWidth:0}]},
options:{
rotation:-90,
circumference:180,
cutout:'70%',
plugins:{legend:{display:false},tooltip:{enabled:false}}
}
});
});
}

setInterval(loadWeek,3000);
setInterval(loadGauge,3000);
loadWeek();
loadGauge();
