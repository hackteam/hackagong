window.insertionPoint = 0;
window.addingTask = 0;
console.log('1');

window.onload = function () {

    $('#addtask').click( function() {
        window.addingTask = 1;
        $('#addtask').html('');
    })

    $('#addlist').click( function() {
        window.addingTask = 1;
        $('#addlist').html('');
    })

    if ($('#addtask').length > 0) {
    var insertionPointHack = setInterval(function(){insertionPoint('addtask')},700);
    }  
    if ($('#addlist').length > 0) {
    var insertionPointHack = setInterval(function(){insertionPoint2('addlist')},700);
    }

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

    function insertionPoint2(divname){
        if (window.addingTask != 0) return;
        if ( window.insertionPoint2 == 0 ){
            window.insertionPoint2 = 1;
            $("#"+divname).html("<p>Type the name of your list here</p>");
        } else {
            window.insertionPoint2 = 0;
            $("#"+divname).html("<p>Type the name of your list here |</p>");
        }                         
    }

    console.log(1);

    $('#addtask-btn').click(function(){
        var textdata = $('#addtask').text();
        $.ajax({type:'POST',
            url: '',
            data: {user_id: null, text: textdata}
        }).done(function(msg) {

        });
    });

    $('#addlist-btn').click(function(){
        var textdata = $('#addlist').text();
        $.ajax({type:'POST',
            url: '',
            data: {user_id: null, text: textdata}
        }).done(function(msg) {

        });
    });

    $('.checkbox-inner').click(function(e){
        var taskid = $(this).attr('id');
        $.ajax({type:'POST',
            url: '',
            data: {task_id: taskid}
        }).done(function(msg) {
            
        });
    });

}
