var myVar;

function myFunction() {
    myVar = setTimeout(showPage, 3000);

}

function poll1() {
        document.getElementById("loader").style.display = "none";
        var myVar = setInterval(poll1, 500);
        $.ajax({
            url: "http://127.0.0.1:8000/celery-progress/task_progress/220/",
            type: "GET",
            success: function(res){
                            clearInterval(myVar);
                            showPage();
                             },
            error: errorFunc, 
            dataType: "json",
            complete: showPage,
        })
};

function Poll(){
    $.post('http://localhost:8000/celery-progress/task_progress/16/', function() {
        alert();  // process results here
        document.getElementById("loader").style.display = "none";
        document.getElementById("myDiv").style.display = "block";
        setTimeout(Poll,2000);
    });
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}

function errorFunc(error) {
  console.log("Worker job still not done." + error.status)
}

