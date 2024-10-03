document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('reservationForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        // Gather form data
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const party_size = document.getElementById('party_size').value;
        const customer_name = document.getElementById('customer_name').value;
        const customer_phone = document.getElementById('customer_phone').value;

        // Send a POST request to reserve a table
        fetch('/reserve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: date,
                time: time,
                party_size: party_size,
                customer_name: customer_name,
                customer_phone: customer_phone
            }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('responseMessage').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('responseMessage').innerText = 'Error making reservation';
        });
    });
});
