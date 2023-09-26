// Password check
document.getElementById("registrationForm").addEventListener("submit", function (event) {
    var password1 = document.getElementById("Password1").value;
    var password2 = document.getElementById("Password2").value;
    var passwordMessage = document.getElementById("passwordMessage");

    if (password1 !== password2) {
        passwordMessage.textContent = "Passwords do not match!";
        event.preventDefault(); // Prevent form submission
    } else {
        passwordMessage.textContent = ""; // Clear error message
    }
});