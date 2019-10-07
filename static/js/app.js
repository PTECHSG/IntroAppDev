$(function() {
    $('button').click(function () {
        console.log("click button");
        $.ajax({
            url: '/checkguess',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
