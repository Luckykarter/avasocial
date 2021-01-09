function authenticate() {
    return new Promise(function(){
        $.ajax({
        xhrFields: {withCredentials: true},
        url: '/user/login/refresh/',
        type: 'POST',
        data: {
            refresh: Cookies.get('refresh')
        },
        success: function(result) {
            localStorage.setItem('access', result.access);
            var res = result.access;
        },
        error: function (error) {
            console.log(error);
        }
    })
    })
}



$( document ).ready(function(){
    
    authenticate().then((res) => console.log(res));

    $('.alert-line').hide();
          
        
    $('.like-up').click(function(){

        let clicked = $(this);

        let post_id = clicked.attr('data-field')
        let likes_field = $('#' + post_id);
        let likes = parseInt(likes_field.text());
        let clicked_flag = likes_field.attr('attr-clicked');
        
        
        
        authenticate().then(like_post(post_id, likes_field));

    })

})



function create_post() {
    post_content = $('#post-content').val();
    authenticate().then(publish(post_content));
}

function publish(content){
    $.ajax({
        url: '/post/create/',
        type: 'POST',
        headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')},
        data:{
            content: content,
        },
        datatype: 'json',
        success: function(result) {
            location.reload();
        },
        error: function (error) {
            console.log(error);
        }
    })
    
}

function like_post(post_id, likes_field){
        $.ajax({
        url: '/post/' + post_id + '/like',
        type: 'GET',
        headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')},
        success: function(result) {
            const likes = parseInt(likes_field.text())
            if (result.message.includes('unliked')){
                likes_field.text( likes - 1 );
            } else {
                likes_field.text( likes + 1 );
            }

        },
        error: function (request, status, error) {
            req = JSON.parse(request.responseText);

            console.log('#alert-line' + post_id)
            $('#alert-text' + post_id).text(req.message);
            $('#alert-line' + post_id).delay(0).show(100);
            $('#alert-line' + post_id).delay(2000).hide(100);
            console.log(error);
        }
    })
}


