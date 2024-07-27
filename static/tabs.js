$(document).ready(function () {
    $('#form2').hide();
    $('.tab-element').on('click', function () {
        var selectedTab = $(this).attr('id');
        
        if (selectedTab === 'tab1') {
            $('#form1').show();
            $('#form2').hide();
        } else if (selectedTab === 'tab2') {
            $('#form1').hide();
            $('#form2').show();
        }
    });
    let form2Button = ".submit-form"

    $(form2Button).on("click", function(){
        let form = $(this).closest("form");
        let textElement = $(form).find("textarea");
        let inputElement = $(form).find("input[type=text]");
        let fileElement = $(form).find("input[type=file]");
        let submit  = true;
        $(textElement).each(function(){
            if($(this).val() == ""){
                submit = false
            }
        })
        $(inputElement).each(function(){
            if($(this).val() == ""){
                submit = false
            }
        })
        $(fileElement).each(function(){
            if($(this).val() !== ""){
                submit = true
            }
        })
        
        if(submit){
            $(form).submit();
        }
    })

    // Toggle share options
    $('.share-btn').on('click', function() {
        // Close other share options
        $('.share-options').not($(this).siblings('.share-options')).hide();
        $(this).siblings('.share-options').toggle();
    });

    // Redirect to share links
    $('.email-share').on('click', function(e) {
        e.preventDefault();
        var chatContent = $(this).closest('.chat-block').data('chat');
        var emailURL = `mailto:?subject=Check this chat&body=${encodeURIComponent(chatContent)}`;
        window.open(emailURL, '_blank');
    });


});