const togglePassword = document.getElementById('togglePassword')
const password = document.getElementById('password')

togglePassword.addEventListener('click', function(){
    const type = password.getAttribute('type') === 'password' ? 'text' :' password'
    password.setAttribute('type', type)

    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});