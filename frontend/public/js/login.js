const togglePassword = document.getElementById('togglePassword')
const password = document.getElementById('password')

togglePassword.addEventListener('click', function(){
    const type = password.getAttribute('type') === 'password' ? 'text' :' password'
    password.setAttribute('type', type)

    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});

async function login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login', {
            method: 'POST',
            body: formData,
        });
        
        if(!response.ok) throw new Error('Email ou senha incorretos');

        window.location.href = 'dashboard.html';

    }catch (error) {
        console.error('Erro no login:', error.message);
    }
}

document.getElementById('submit').addEventListener('submit', function(e) {
    e.preventDefault();
    const emailValue = document.getElementById('email').value;
    const passwordValue = document.getElementById('password').value;
    
    login(emailValue, passwordValue);
});