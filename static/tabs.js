$(document).ready(function () {
    console.log("Hi");
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
});