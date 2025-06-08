document.querySelector('#order-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });

    const data = await response.json();
    if (data.success) {
        window.location.href = data.redirect_url;
    } else {
        // Показать ошибки валидации
    }
});