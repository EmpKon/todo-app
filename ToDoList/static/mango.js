function addTask() { //Adds a task to the sqlite database 
    var value = document.getElementById("taskInput").value;
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