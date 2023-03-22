// BTT button
$(function () {
    $('#BackTop').click(function () {
        $('html,body').animate({scrollTop: 0}, 500);
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#BackTop').fadeIn(300);
        } else {
            $('#BackTop').stop().fadeOut(300);
        }
    }).scroll();
});

$(function(){
    $(".reply-link").click(function(e){
        if ( $("#reply-input").length > 0 ) { 
            $("#reply-input").remove();
        }else{
            let replyArea = "<li id='reply-input' class='list-group-item'><div class='input-group'><input type='text' id='reply' class='form-control'></input><button type='submit' class='btn btn-primary'>send</button></div></li>";
            $(e.target).parent().append(replyArea);
            $("#reply").val("@" + $(e.target).parent().children()[0].innerHTML);
        }              
    });
});