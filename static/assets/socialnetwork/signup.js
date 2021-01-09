 $(document).ready(function() {
     $('#alert-line').hide();
     $('#success-line').hide();

    $("#form-signup").submit(function(e){
        $('#alert-line').hide(20);
        $('#success-text').text('Loading...');
        $('#success-line').show(20);
        e.preventDefault(e); 
        submit_form();

    });
});

    function submit_form(){

        $.ajax({
            url: '/user/signup/',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                user:{
                    username: $('#username').val(),
                    password: $('#password1').val()
                },
                email: $('#email').val()
            }),
            datatype: 'json',
            success: function(result) {
                localStorage.setItem('username', $('#username').val());
                window.location.href = "/";

            },
            error: function (request, status, error) {
                $('#success-line').hide(0);
                req = JSON.parse(request.responseText);
                $('#alert-text').text(req.message);
                $('#alert-line').show(20);

            }
        })
    }