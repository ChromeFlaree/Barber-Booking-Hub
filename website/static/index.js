document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = "opacity 1s";
            alert.style.opacity = "0";
        }, 3000);

        setTimeout(function() {
            alert.remove();
        }, 4000);
    });
});