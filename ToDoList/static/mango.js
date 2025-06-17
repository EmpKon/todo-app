stateCycle = {
    "not_started": "in_progress",
    "in_progress": "complete",
    "complete": "not_started"
};

themes = [
    ["#4A102A", "#85193C", "#C5172E", "#FCF259", "#cfc64a"],
    ["#B33791", "#C562AF", "#DB8DD0", "#FEC5F6", "#cfc64a"],
    ["#FFB200", "#EB5B00", "#D91656", "#640D5F", "#cfc64a"],
    ["#FDFBEE", "#57B4BA", "#015551", "#FE4F2D", "#cfc64a"],
    ["#FBDB93", "#BE5B50", "#8A2D3B", "#641B2E", "#cfc64a"]
]

var r = document.querySelector(':root');

function setTheme(index) {
    r.style.setProperty('--bgColor', themes[index][0]);
    r.style.setProperty('--boxbgColor', themes[index][1]);
    r.style.setProperty('--accentColor', themes[index][2]);    
    r.style.setProperty('--txtColor', themes[index][3]);
    r.style.setProperty('--progressColor', themes[index][4]);
}

function addTask() { //Adds a task to the sqlite database 
    var value = document.getElementById("taskInput").value;
    document.getElementById("taskInput").value = "";
    $.ajax({
        url: "/addData",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({ 'value': value }),
        success: function(response) {
            console.log("Task added!")
        },
        error: function(error) {
            console.log(error);
        }
    });
    setTimeout(displayTasks, 10); //Slight delay to account for the time that it takes for the task to get added to the sqlite db
}

function removeData(taskID) {
        $.ajax({
        url: "/removeData",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({ "id" : taskID }),
        success: function(response) {
            console.log("Task removed")
        },
        error: function(error) {
            console.log(error);
        }
    });
    setTimeout(displayTasks, 10); //Slight delay to account for the time that it takes for the task to get deleted from the sqlite db
}

function cycleStatus(taskID, status) {
    let newstatus = stateCycle[status]
        $.ajax({
        url: "/cycleStatus",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({ "id" : taskID, "status" : newstatus}),
        success: function(response) {
            console.log("Status changed")
        },
        error: function(error) {
            console.log(error);
        }
    });
    setTimeout(displayTasks, 10); //Slight delay to account for the time that it takes for the task to get deleted from the sqlite db
}


function displayTasks() { 
    fetch("/getData") //Fetches all the saved tasks from the database
        .then(data => data.json())
        .then(data => {
            console.log(data);
            document.getElementById("taskTable").innerHTML = ""
            for (let i = 0; i < data.length; i++) { //Adds tasks to table
                document.getElementById("taskTable").innerHTML += //Suddenly works after fixing a typo ToT
                `<tr>
                <td class="${data[i][2]} taskItem">
                <a href="#" onclick="cycleStatus(${data[i][0]}, '${data[i][2]}')">
                ${data[i][1]}&emsp;&emsp;&emsp; ${data[i][2]}&emsp;&emsp;&emsp; <button onclick="removeData(${data[i][0]})">Delete</button>
                </a>
                </td>
                </tr>
                `
            }});
        }

window.addEventListener("DOMContentLoaded", (event) => {
    document.getElementById("taskInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && document.getElementById("taskInput").value != "") {
            document.getElementById("addButton").click();
        }
    });
});
