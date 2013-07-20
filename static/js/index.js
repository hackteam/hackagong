window.insertionPoint = 0;
window.addingTask = 0;
console.log('1');

window.onload = function () {

    $('#addtask').click( function() {
        window.addingTask = 1;
        $('#addtask').html('');
    })

        
    var insertionPointHack = setInterval(function(){insertionPoint('addtask')},700);
    function insertionPoint(divname){
        if (window.addingTask != 0) return;
        if ( window.insertionPoint == 0 ){
            window.insertionPoint = 1;
            $("#"+divname).html("<p>Type your task here</p>");
        } else {
            window.insertionPoint = 0;
            $("#"+divname).html("<p>Type your task here |</p>");
        }                         
    }
    console.log(1);

}
