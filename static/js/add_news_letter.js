$(document).ready(function () {
    function add_email_news_letter_click() {
        // $(document).on('submit', '#newletter_email', function (e) {
        var email_newsletter = $("#add_email_news_letter").val();
        console.log(email_newsletter);
        $.ajax({
            url: '{% url "add_newsletter_email" %}',
            data: {
                'email_newsletter': email_newsletter,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'email_for_letter': 'Yes'
            },
            dataType: 'json',
            success: function (data) {
                console.log(data.email_registered);
                if (data.email_registered) {
                    // alert("A user with this username already exists.");
                    Swal.fire({
                        position: 'top-end',
                        icon: 'error',
                        title: 'Email already registered',
                        showConfirmButton: false,
                        timer: 1500
                    })
                }
                else {
                    Swal.fire({
                        position: 'top-end',
                        icon: 'success',
                        title: 'Congratulations, you will be hearing from us shortly',
                        showConfirmButton: false,
                        timer: 1500
                    })
                }
            }
        });
    }
});