function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function apiFetch(endpoint, options = {}) {
    const token = getCookie('access_token');
    
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };

    const response = await fetch(`http://127.0.0.1:8000/api/v1${endpoint}`, {
        ...options,
        headers: headers,
        credentials: 'include'
    });

    if (response.status === 401) {
        window.location.href = 'login.html';
        return;
    }

    return response;
}