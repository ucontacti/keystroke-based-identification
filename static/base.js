var input = "michael mock"
var atDown = 0
var atUp = 0
var timeDown = [];
var timeUp = [];
var test = false;
var session = 0;
var try_num = 0;
var session_time_down = []
var session_time_up = []


function init_variables() {
    $.post("/init", function (result) {
        session = result['session'];
        document.getElementById("p2").innerHTML = "session: " + session;
    });
}

function call_train() {
    if (session < 10) {
        document.getElementById("p1").innerHTML = "try: " + try_num;
        document.getElementById("p1").style.display = "block";
        document.getElementById("in_text").style.display = "block";
        test = false;
    }
    else {
        var r = confirm("You already have 10 sessions, do you want to send us and reset?");
        if (r == true) {
            upload_data();
        }
    }
}

function del_data(confidence) {
    if (!confidence)
    {
        var r = confirm("Are you sure you want to delete your Data?");
        if (r == true) {
            $.post("/del_data");
            var x = document.getElementById("del_snackbar");
            x.className = "show";
            setTimeout(function () { x.className = x.className.replace("show", ""); }, 2000);
            session = 0;
            call_res_session();
        }
    }
    else{
        $.post("/del_data");
        var x = document.getElementById("del_snackbar");
        x.className = "show";
        setTimeout(function () { x.className = x.className.replace("show", ""); }, 2000);
        session = 0;
        call_res_session();
    }
}

function download_data() {
    $.post("/download/time.csv", function (result) {
        if (result['status'] != "file not exist") {
            var blob = new Blob([result]);
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = "keystroke_data.csv";
            link.click();
        }
        else {
            var x = document.getElementById("nofile_snackbar");
            x.className = "show";
            setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
        }
    });
}

function upload_data() {
    if (session < 10) {
        alert("You have not finished 10 sessions!");
    }
    else {
        $.post("/upload/time.csv", function (result) {
            if (result['status'] != "file not exist") {
                del_data(true);
                var x = document.getElementById("upload_snackbar");
                x.className = "show";
                setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
            }
            else {
                var x = document.getElementById("nofile_snackbar");
                x.className = "show";
                setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
            }
        });
    }
}

function call_test() {
    document.getElementById("in_text").style.display = "none";
    document.getElementById("p1").style.display = "none";
    test = true;
    var x = document.getElementById("auth_snackbar");
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}

function keyDown(event) {
    var key = String.fromCharCode(event.keyCode).toLowerCase();
    var keycode = event.keyCode;
    var valid =
        (keycode > 47 && keycode < 58) || // number keys
        keycode == 32 || keycode == 13 || // spacebar & return key(s) (if you want to allow carriage returns)
        (keycode > 64 && keycode < 91) || // letter keys
        (keycode > 95 && keycode < 112) || // numpad keys
        (keycode > 185 && keycode < 193) || // ;=,-./` (in order)
        (keycode > 218 && keycode < 223); // [\]' (in order)
    if (valid) {
        if (input.charAt(atDown) == key) {
            timeDown.push(performance.now());
            atDown++;
        } else {
            wrong();
        }
    }
}


function keyUp(event) {
    var key = String.fromCharCode(event.keyCode).toLowerCase();
    var keycode = event.keyCode;
    var valid =
        (keycode > 47 && keycode < 58) || // number keys
        keycode == 32 || keycode == 13 || // spacebar & return key(s) (if you want to allow carriage returns)
        (keycode > 64 && keycode < 91) || // letter keys
        (keycode > 95 && keycode < 112) || // numpad keys
        (keycode > 185 && keycode < 193) || // ;=,-./` (in order)
        (keycode > 218 && keycode < 223); // [\]' (in order)

    if (valid) {
        if (input.charAt(atUp) == key) {
            timeUp.push(performance.now());
            atUp++;
        } else {
            wrong();
        }
        if (atUp == input.length) {
            try_num += 1;
            document.getElementById("p1").innerHTML = "try: " + try_num;
            session_time_down.push(timeDown);
            session_time_up.push(timeUp);
            if (try_num == 5) {
                if (test) {
                    $.post("/post_test", {
                        down_time_data: JSON.stringify(session_time_down),
                        up_time_data: JSON.stringify(session_time_up)
                    });
                } else {
                    $.post("/post_data", {
                        down_time_data: JSON.stringify(session_time_down),
                        up_time_data: JSON.stringify(session_time_up)
                    });
                }
                session += 1;
                if (session == 10) {
                    alert("You have successfuly finished all 10 sessions. You can send us your data now.");
                }
                else {
                    alert("You finished the session. It is better to take new session in another time");
                }
                call_res_session();
            }
            reset();
            var x = document.getElementById("done_snackbar");
            x.className = "show";
            setTimeout(function () { x.className = x.className.replace("show", ""); }, 2000);
        }
    }
}

function wrong() {
    var x = document.getElementById("error_snackbar");
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 1000);
    reset();
}

function reset() {
    document.getElementById("in_text").value = "";
    atDown = atUp = 0;
    timeDown = [];
    timeUp = [];
}

function call_res_session() {
    reset();
    session_time_up = [];
    session_time_down = [];
    try_num = 0;
    document.getElementById("in_text").style.display = "none";
    document.getElementById("p1").style.display = "none";
    document.getElementById("p2").innerHTML = "session: " + session;
}