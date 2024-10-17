<h1>Data Flow Diagram</h1>

![Data Flow Diagram](https://github.com/user-attachments/assets/6ca5d2d8-c8a6-4bce-8a8e-63ee22e1b47d)
<h4>Below signifies four distinct processes our application will take when dealing with bookings</h4>
<p>We have labelled four processes instead of an actual text description as the diagram depicts how the majority of the system will process requests from the user</p>
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
<h1>Conceptual Entity Relationship Diagram</h1>
![Entity Relationship Diagram](https://github.com/user-attachments/assets/49dbefa5-2347-41c3-9f2a-2e5667992df9)
<p>The Table Reservation System consists of several key entities that interact to allow customers to easily manage their bookings. The primary entities are <b>Users</b>, <b>Reservations</b>, <b>Restaurants</b>, <b>Tables</b> and <b>Notifications</b></p>
<h4>User Attributes</h4>
<ul>
  <li><b>User ID</b> - Primary key, unique identifier for each user</li>
  <li><b>Name, Email and Phone</b> - User contact details</li>
</ul>
<h4>Reservation Attributes</h4>
<ul>
  <li><b>Reservation ID</b> - Primary key, unique identifier for each reservation</li>
  <li><b>User ID</b> - Foreign key linking the reservation to a user</li>
  <li><b>Table ID</b> - Foreign Key linking the reservation to a table</li>
  <li><b>Restaurant ID</b> - Foreign key linking the reservation to the restaurant </li>
  <li><b>Date and Time</b> - Date and time of the reservation</li>
  <li><b>Guests</b> - Number of guests for the reservation</li>
  <li><b>Preferences</b> - Any special requests/requirements from the user</li>
  <li><b>Status</b> - Indicates the reservation status (confirmed, modified, cancelled)</li>
</ul>
<h4>Restaurant Attributes</h4>
<ul>
  <li><b>Restaurant ID</b> - Primary key, unique identifier for each location</li>
  <li><b>Name and Address</b> - Details about the restaurant</li>
</ul>
<h4>Table Attributes</h4>
<ul>
  <li><b>Table ID</b> - Primary key, unique identifier for each table</li>
  <li><b>Restaurant ID</b> - Foreign key linking the table to a restaurant</li>
  <li><b>Table Number</b> - Unique identifier for the table within the restaurant</li>
  <li><b>Capacity</b> - Maximum number of guests the table can accommodate</li>
  <li><b>Status</b> - Indicates the table status (available, booked, under maintenance)</li>
  <li><b>Location</b> - Indicates whether the table is indoors or outdoors</li>
</ul>
<h4>Notification Attributes</h4>
<ul>
  <li><b>Notification ID</b> - Primary key, unique identifier for each notification</li>
  <li><b>User ID</b> - Foreign key linking the notification to a user</li>
  <li><b>Reservation ID</b> - Foreign key linking the notification to a specific reservation</li>
  <li><b>Message</b> - Content of the notification (booking confirmation or reminder)</li>
</ul>
<h2>Entity Relations</h2>
<ul>
  <li>A <b>User</b> can create multiple <b>Reservations</b>, creating a one-to-many relationship.</li>
  <li>Each <b>Reservation</b> is associated with one <b>Table</b> and one <b>Restaurant</b>, creating a many-to-one relationship from <b>Reservation</b> to both <b>Table</b> and <b>Restaurant</b>.</li>
  <li>A <b>Restaurant</b> can have multiple <b>Tables</b>, creating a one-to-many relationship.</li>
  <li>Each <b>Notification</b> is linked to a specific <b>User</b> and a specific <b>Reservation</b>, creating a many-to-one relationship from <b>Notification</b> to both <b>User</b> and <b>Reservation</b>.</li>
</ul>
