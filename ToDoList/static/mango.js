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
    })


}

function displayTasks() { 
    var table = document.getElementById("taskable")
    fetch("/getData") //Fetches all the saved tasks from the database
        .then(data => data.json())
        .then(data => {
            console.log(data);
        });

}