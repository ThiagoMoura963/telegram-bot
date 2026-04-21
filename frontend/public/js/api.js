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

    const response = await fetch(``, {
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