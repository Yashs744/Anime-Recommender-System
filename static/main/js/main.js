
(function ($) {
    "use strict";

    if($('#id_username').val().trim() !== "") {
        $('#id_username').addClass('has-val');
    }
    $('#id_username').on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    });

    if($('#id_email').val().trim() !== "") {
        $('#id_email').addClass('has-val');
    }
    $('#id_email').on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    });

    $('#id_password').on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    });

    $('#id_password1').on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    });

    $('#id_password2').on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    });

})(jQuery);