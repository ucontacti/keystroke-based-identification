var input = "michael mock"
var atDown = 0
var atUp = 0
var timeDown = [];
var timeUp = [];
var test = false;

function call_train() {
    document.getElementById("in_text").style.display = "block";
    test = false;
}

function call_test() {
    document.getElementById("in_text").style.display = "none";
    test = true;
    var x = document.getElementById("auth_snackbar");
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}

function keyDown(event) {
    var key = String.fromCharCode(event.keyCode).toLowerCase();
    var keycode = event.keyCode;
    var valid =
        (keycode > 47 && keycode < 58) ||    // number keys
        keycode == 32 || keycode == 13 || // spacebar & return key(s) (if you want to allow carriage returns)
        (keycode > 64 && keycode < 91) || // letter keys
        (keycode > 95 && keycode < 112) || // numpad keys
        (keycode > 185 && keycode < 193) || // ;=,-./` (in order)
        (keycode > 218 && keycode < 223);   // [\]' (in order)
    if (valid) {
        if (input.charAt(atDown) == key) {
            timeDown.push(performance.now());
            atDown++;
        }
        else {
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
        (keycode > 218 && keycode < 223);   // [\]' (in order)

    if (valid) {
        if (input.charAt(atUp) == key) {
            timeUp.push(performance.now());
            atUp++;
        }
        else {
            wrong();
        }
        if (atUp == input.length) {
            var x = document.getElementById("done_snackbar");
            x.className = "show";
            setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
            if (test) {
                $.post("/post_test", {
                    down_time_data: JSON.stringify(timeDown),
                    up_time_data: JSON.stringify(timeUp)
                });
            }
            else {
                $.post("/post_data", {
                    down_time_data: JSON.stringify(timeDown),
                    up_time_data: JSON.stringify(timeUp)
                });
            }
            reset();
        }
    }
}

function wrong() {
    var x = document.getElementById("error_snackbar");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
    reset();
}

function reset() {
    document.getElementById("in_text").value = "";
    atDown = atUp = 0;
    timeDown = timeUp = []
}