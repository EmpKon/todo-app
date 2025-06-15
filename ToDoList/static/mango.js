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
    setTimeout(displayTasks, 100); //Slight delay to account for the time that it takes for the task to get added to the sqlite db
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
    setTimeout(displayTasks, 100); //Slight delay to account for the time that it takes for the task to get deleted from the sqlite db
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
                <td>
                ${data[i][1]}&emsp;&emsp;&emsp; <button onclick="removeData(${data[i][0]})">Delete</button>
                </td>
                </tr>` //TODO: Make clearTask function for this to remove from db
            }});
        }

window.addEventListener("DOMContentLoaded", (event) => {
    document.getElementById("taskInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && document.getElementById("taskInput").value != "") {
            document.getElementById("addButton").click();
        }
    });
});
