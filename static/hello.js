var input = "michael mock"
var atDown = 0
var atUp = 0
var timeDown = [];
var timeUp = [];


function sayHello() {
    alert("Hello World!");
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
    if (valid)
    {
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
            $.post( "/postmethod", {
                down_time_data: JSON.stringify(timeDown),
                up_time_data: JSON.stringify(timeUp)
            });
            reset();
        }
    }
}

function wrong() {
    alert("Something went wrong!");
    document.getElementById("in_text").value = "";
    reset();
}

function reset(){
    atDown = atUp = 0;
    timeDown = timeUp = []
}