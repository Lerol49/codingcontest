

function closeAlert() {
  document.getElementById("flash_alert").remove();
}

var till_time = 36000;
var end_time = 0;
var cur_time = parseInt(Date.now()/1000);

window.addEventListener("load", (event) => {
    var path = window.location.pathname;
    var contest_id = "the_beginning"

    var stored = localStorage.getItem("end_time");



    if (stored && stored != 0) {
        end_time = stored;
        till_time = end_time - cur_time;

    } else {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", "/contest/" + contest_id + "/get_end_time", false ); // false for synchronous request
        xmlHttp.send( null );

        end_time = parseInt(xmlHttp.responseText);

        till_time = end_time - cur_time;

        localStorage['end_time'] = end_time;
    }

    till_time = Math.max(0, till_time);

    hours = Math.floor((till_time / 3600) % 3600);
    if (hours < 10) {
        hours = "0" + hours;
    }

    minutes = Math.floor((till_time / 60) % 60);
    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    seconds = Math.floor(till_time % 60);
    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    document.getElementById("timer").innerHTML = hours + ":" + minutes + ":" + seconds;





});



a = setInterval(updateTimer, 1000);

function updateTimer() {

    hours = Math.floor((till_time / 3600) % 3600);
    if (hours < 10) {
        hours = "0" + hours;
    }

    minutes = Math.floor((till_time / 60) % 60);
    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    seconds = Math.floor(till_time % 60);
    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    document.getElementById("timer").innerHTML = hours + ":" + minutes + ":" + seconds;
    till_time -= 1;


    if (till_time < 0) {
        clearInterval(a);
    }
}
