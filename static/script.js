$("#success").hide();
$("#failure").hide();

function changeStateOfLight(url){
$.ajax(url)
    .done(function(data, text, request) {
        $("#success_status_code").text( "Code -> " + request.status);
        $("#success").show();
    })
    .fail(function(data, text, request) {
        $("#failure_status_code").text(request.status);
        $("#failure").show();
    })
    .always(function() {
        setTimeout(function(){
           location.reload()
        }, 500);
    });
}