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
}

function send_data() {
    document.getElementById("in_text").style.display = "none";
    $.post("/post_send_data");
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
        (keycode > 218 && keycode < 223);   // [\]' (in order)
    if (valid) {
        if (input.charAt(atDown) == key) {
            timeDown.push(performance.now());
            atDown++;
        }
        else {
            console.log(atDown);
            console.log("down issue" + input.charCodeAt(atDown) + " " + key)
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
            console.log(atUp);
            console.log("up issue " + input.charCodeAt(atUp) + " " + key)
            wrong();
        }
        if (atUp == input.length) {
            alert("Done!");
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
    alert("Something went wrong!");
    reset();
}

function reset() {
    document.getElementById("in_text").value = "";
    atDown = atUp = 0;
    timeDown = timeUp = []
}