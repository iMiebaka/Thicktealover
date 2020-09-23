$(document).ready(function () {
function log_out() {
    console.log('Hello');
    
    Swal.fire({
      title: 'Logging out?',
      text: "You are just about to logout!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, Logout ASAP!'
    }).then((result) => {
      if (result.value) {
        window.location.href = "{% url 'logout_view' %}";
      }
    })
  }
})