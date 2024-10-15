<h1>Data Flow Diagram</h1>

![Data Flow Diagram](https://github.com/user-attachments/assets/6ca5d2d8-c8a6-4bce-8a8e-63ee22e1b47d)
<h4>Below signifies four distinct processes our application will take when dealing with bookings</h4>
<p>We have labelled four proccesses instead of a actual text description as the diagram depicts how the majority of the system will process requests from the user</p>
<ul>
  <h4>Process 1)</h4>
  <li>1a) User inputs details to make a reservation</li>
  <li>1b) User modifies an existing reservation to select a different date and time</li>
  <li>1c) User deletes an existing reservation</li>
  <li>1d) User is put into a waiting list until a reservation becomes free</li>
</ul>
<ul>
  <h4>Process 2)</h4>
  <li>Based on 1a,1b,1c and 1d, the users request is sent to the API</li>
</ul>
<ul>
  <h4>Process 3)</h4>
  <li>Based on the API request the database responds accordingly with the correct information which is then passed back to the API (conditions 1a,1b,1c and 1d)</li>
</ul>
<ul>
  <h4>Process 4)</h4>
  <li>The APIs response is jsonified and presented to the user in a string format (conditions 1a,1b,1c and 1d)</li>
</ul>
<h1>Entity Relationships</h1>
![table reservation erd](https://github.com/user-attachments/assets/bc0ea5a0-5327-4c1d-ba07-f2e99c54d6f0)
<h4>Conceptual Entity Relationship Diagram</h4>
<p>The Table Reservation System consists of several key entities that interact to allow for customers to easily manage their bookings. The primary entities are **Users**, **Reservations**, **Restaurants**, **Tables** and **Notifications**</p>
<h4>User Attributes</h4>
<ul>
  <li>User ID - Primary key, unique identifier for each user</li>
  <li>Name, Email and Phone - user contact details</li>
</ul>
<h4>Reservation Attributes</h4>
<ul>
  <li>Reservation ID - Primary key, unique indentifier for each reservation</li>
  <li>User ID - Foreign key linking the reservation to a user</li>
  <li>Table ID - Foreign Key linking the reservation to a table</li>
  <li>Restauant ID - Foreign key linking the reservation to the restuarant</li>
  <li>Date - </li>
</ul>
<h4>Restaurant Attributes</h4>
<ul>

</ul>
<h4>Table Attributes</h4>
<ul>
  
</ul>
<h4>Notification Attributes</h4>
<ul>
  
</ul>
<h4> </h4>
