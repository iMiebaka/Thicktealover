$(document).ready(function () {
    var tag_alert = '{{ message.tags }}';
    if (tag_alert == 'alert-success') {
        tag_alert = 'success';
    }
    if (tag_alert == 'alert-danger') {
        tag_alert = 'error';
    }
    Swal.fire({
        position: 'top-end',
        icon: tag_alert,
        title: '{{ message }}',
        showConfirmButton: false,
        timer: 1500
})