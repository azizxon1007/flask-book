document.getElementById('guestbook-form').onsubmit = async function(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let response = await fetch('/sign', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        location.reload();
    } else {
        let result = await response.json();
        alert(result.errors.name || result.errors.message);
    }
};

document.querySelectorAll('.delete').forEach(function(button) {
    button.onclick = async function(event) {
        let entryId = this.getAttribute('data-id');
        let response = await fetch(`/delete/${entryId}`, {
            method: 'POST'
        });

        if (response.ok) {
            location.reload();
        }
    };
});
