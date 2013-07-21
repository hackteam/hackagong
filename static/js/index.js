window.insertionPoint = 0;
window.addingTask = 0;

window.onload = function () {

        $('.landing-btn').mouseover(function () {
            $('.circle').addClass("open");
            //$('.subtitle2').animate({opacity:0});
        });

        $('.landing-btn').mouseout(function () {
            $('.circle').removeClass("open");
    //        $('.subtitle2').animate({opacity:1});
        });

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

    function showform(){
        $(".hiddenform").animate({'height': '300px'}, 400);
        $(".hiddenform form").fadeIn(400)
    }

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

    function swishy(elem) {
        elem.find(".tick").css({display: "inline-block"});
    }

        $('.mainbox').on('click','.checkbox',function(e){
            console.log("Clicked");
            var taskid = $(this).parent().attr('task-id');
            var elem = $(this);
            $.ajax({type:'POST',
                url: '/finishtask/' + taskid,
                data: {task_id: taskid},
                success: function(output) {
                  console.log(output);
                  if (output == 'success') {
                    elem.find(".tick").css({display: "inline-block"});
                    elem.parent().animate({width: 0}, 500, function(){ $(this).slideUp(200) })
                  } else {
                    alert('Login info incorrect');
                  }
                },
                error: function(output) {
                  alert('error: please refresh');
                  console.log(output);
                }
            });
        });

    $('.startr').click(function(e){
        $(this).fadeOut(200, showform);
    })

    function showform(){
        $(".hiddenform").animate({'height': '300px'}, 400);
        $(".hiddenform form").fadeIn(400)
    }

    $('.startr').click(function(e){
        $(this).fadeOut(200, showform);
    })

}
