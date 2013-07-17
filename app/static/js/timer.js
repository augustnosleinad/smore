
<script language="Javascript">

var h=00;var m=00;var s=00;  /* initial timer values */
var mup, hup;  /* for incremeting minutes and hours */
var running = false;  /* timer state status */

function start(){
	if (running == false){
			var timer = setInterval("ticking()",1000);
			running = true;
	}
}

function pause(){
	clearInterval(timer); /* stop calls to ticking()*/
	running = false;
}

function stop(){
	clearInterval(timer); /* stop calls to ticking() */
	h=00; m=00; s=00;
	document.getElementById('tickHours').innerHTML=h;
	document.getElementById('tickMinutes').innerHTML=m;
	document.getElementById('tickSeconds').innerHTML=s;
	running = false;
}

function ticking()   /* called every second  */
{
	if(s<59){s=s+01;mup=false;hup=false;}
	else if(s==59){s==00;mup=true;hup=false}

	if(mup==true&&m<59){m=m+01;}
	else if(mup==true&&m==59){m=00;hup=true;}

	if(hup==true&&h<23){h=h+01;}
	else if(hup==true&&h==23){h==00;}

	document.getElementById('tickHours').innerHTML=h;
	document.getElementById('tickMinutes').innerHTML=m;
	document.getElementById('tickSeconds').innerHTML=s;
}

</script>