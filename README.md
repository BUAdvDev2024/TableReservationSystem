<h1>Table Reservation System</h1>
<p>This repository will allow users to make table reservations depending on the availability of the restaurant. For this we will be creating an API which will interact with a database.</p>
<br>
<h1>Requirements</h1>
<ul>
  <li>Users should be able to select a date, time, and number of people for their reservation.</li>
  <li>Users would expect to be able to change or cancel their booking if plans change.</li>
  <li>Users should be able to see if the selected date and time have tables available</li>
  <li>Users should be able to cancel a booking</li>
  <li>Once the booking is successful, users could get an immediate confirmation message or email with reservation details.</li>
  <li>The system should prompt the user to enter their name, email, and phone number for confirmation and communication.</li>
  <li>Users would expect that their personal details are handled securely and are not misused.</li>
  <li>Users could expect to receive a reminder email or SMS closer to the reservation time.</li>
  <li>Users could add in a special message such as dietary preferences, high chair requests, or seating preferences (e.g., indoor/outdoor).</li>
  <li>If no tables are available at their preferred time, users could opt to join a waitlist.</li>
</ul>
<br>
<h1>Data Flow Diagram</h1>
<h4>Below signifies four distinct processes our application will take when dealing with bookings</h4>
<p>We have labelled four proccesses instead of a actual text description as the diagram depicts how the majority of the system will process requests from the user</p>
<ul>
  <h4>Process 1)</h4>
  <br>
  <li>1a) User inputs details to make a reservation</li>
  <li>1b) User modifies an existing reservation to select a different date and time</li>
  <li>1c) User deletes an existing reservation</li>
  <li>1d) User is put into a waiting list until a reservation becomes free</li>
</ul>
<ul>
  <h4>Process 2)</h4>
  <br>
  <li>Based on 1a,1b,1c and 1d, the users request is sent to the api</li>
</ul>
<ul>
  <h4>Process 3)</h4>
  <br>
  <li>Based on the API request the database responds accordingly with the correct information which is then passed back to the API (conditions 1a,1b,1c and 1d)</li>
</ul>
<ul>
  <h4>Process 4)</h4>
  <br>
  <li>The APIs response is jsonified and presented to the user in a string format (conditions 1a,1b,1c and 1d)</li>
</ul>
![image](https://github.com/user-attachments/assets/de2377b7-80ec-4007-91e8-c59e1ab3cb4e)
<br>
<h1>Entity Relationship</h1>



