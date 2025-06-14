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
    fetch("/getData") //Fetches all the saved tasks from the database
        .then(data => data.json())
        .then(data => {
            console.log(data); //Prints tasks to console
            for (let i = 0; i < data.length; i++) { //For loop that goes over all the items in the array and adds them to the table
            document.getElementById("taskTable").innerHTML += //Suddenly works after fixing a typo ToT
            `<tr>
                <td>
                    ${data[i]}
                </td>
            </tr>`
        }});
}