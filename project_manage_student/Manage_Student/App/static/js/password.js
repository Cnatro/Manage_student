$(document).ready(function(){
    $('.toggle-show-password').on('click',function(){
        if($('#password').attr('type') === 'password' ){

            $('#password').attr('type','text');
            $(this).removeClass('fa-eye-slash').addClass('fa-eye');
        }else{

             $('#password').attr('type','password');
             $(this).removeClass('fa-eye').addClass('fa-eye-slash');
        }
    });
});