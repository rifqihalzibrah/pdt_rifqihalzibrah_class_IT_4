function convertScore() {
    var score = document.getElementById("score").value;

    var url = "/convert_score";  // url for the python
    axios({
        method: "post",
        url: url,
        data: {
            score: score,
        },
        headers: {
            "Content-Type": "application/json",
        },
    }).then(
        (response) => {
            var result = response.data;
            document.getElementById("convert_score_result").value = result["result"];
        },
        (error) => {
            console.log(error);
        }
    );
}

function squareRoot() {
    var number = document.getElementById("square_root_number").value;

    var url = "/square_root";  // url for the python
    axios({
        method: "post",
        url: url,
        data: {
            number: number,
        },
        headers: {
            "Content-Type": "application/json",
        },
    }).then(
        (response) => {
            var result = response.data;
            document.getElementById("square_root_result").value = result["result"];
        },
        (error) => {
            console.log(error);
        }
    );
}

function hypotenuse() {
    var baseNumber = document.getElementById("base").value;
    var altitudeNumber = document.getElementById("altitude").value;

    var url = "/hypotenuse";  // url for the python
    axios({
        method: "post",
        url: url,
        data: {
            baseNumber: baseNumber,
            altitudeNumber: altitudeNumber,
        },
        headers: {
            "Content-Type": "application/json",
        },
    }).then(
        (response) => {
            var result = response.data;
            document.getElementById("hypotenuse_result").value = result["result"];
        },
        (error) => {
            console.log(error);
        }
    );
}