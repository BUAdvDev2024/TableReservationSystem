# Table Reservation System Test Plan

## Introduction
This test plan outlines the testing strategy and specific test cases for the Table Reservation System. The primary goal is to provide a systematic approach to identifying and addressing potential defects or issues within the system. The objectives of this test plan are:
- Defining the scope of modules to be tested.
- Outlining the testing approach and methodologies.
- Establishing timelines for each testing phase.
- Identifying potential risks and their severity.
- Proposing mitigation strategies for identified risks.

## Testing Resources
Fernando Lopez and I will both be responsible for testing the Table Reservation System. This test plan will guide and coordinate our testing efforts, ensuring that all components of the application are thoroughly evaluated. Through regular communication, we will collaborate to allocate responsibilities, ensuring that every module within the system is tested. Our goal is to achieve comprehensive test coverage and efficient testing cycles.

## Scope of Testing
### In-Scope Modules:
1. Making a booking: Ensures users can book a table with accurate details.
2. Table availability: Verifies correct availability for selected dates/times.
3. Cancelling a booking: Ensures users can cancel existing reservations.
4. Modifying a booking: Allows users to update reservation details.
5. Confirmation of booking: Sends users a booking confirmation via text/email.
6. Waiting list functionality: Adds users to a waiting list when tables are full.
7. Performance testing: Ensures stability and speed during high traffic.
8. Text/Email reminders: Sends reminders before the booking event.

### Out-of-Scope Modules:
1. Mobile responsiveness: Testing UI and experience on different devices.
2. Cross-browser testing: Ensuring the system works across different browsers.
3. Payment APIs: Payment processing and integration with external APIs.

## Testing Approaches

### Approach 1 - White-Box Testing
White-box testing will be used for CRUD functionalities (creating, updating, deleting bookings) to evaluate the internal logic of the code. Given that we are using a Python backend and a SQL database for table bookings, this testing approach will allow us to ensure that the internal structures (e.g., loops, conditions) work as expected.

#### Areas of Focus:
- Double bookings: Verifying that users cannot book the same table at the same time.
- Memory overflow: Ensuring proper memory management during heavy booking activity.
- Booking availability: Validating correct handling of table availability during busy periods.

#### Risks:
- **Risk:** Complex logic or database queries might lead to performance bottlenecks.
- **Mitigation:** Regular code reviews and writing efficient SQL queries.

### Approach 2 - Functional Testing
Functional testing will ensure that the Table Reservation System meets the specified requirements. This includes verifying that users can book, modify, and cancel reservations, and that confirmation messages are sent correctly via text or email.

#### Example:
- Text/Email confirmations: After users complete a booking, they should receive a confirmation message. If the user has an account, they will not need to input contact details for future bookings, reducing friction in the process.

#### Risks:
- **Risk:** Text messages or emails may fail to send due to incorrect user input or integration issues with external SMS/Email services.
- **Mitigation:** Test cases will validate correct data handling and ensure fallback mechanisms (e.g., retrying failed messages).

### Approach 3 - Performance Testing
Performance testing will focus on ensuring the system handles high traffic during peak usage times. The aim is to simulate multiple users booking tables at the same time to evaluate the system’s responsiveness, database performance, and how quickly booking confirmations are processed.

#### Areas of Focus:
- Load testing: Simulate high traffic and concurrent booking requests.
- Response times: Ensure that bookings are processed, and confirmation texts/emails are sent promptly, even under heavy load.

#### Risks:
- **Risk:** The system may experience slow response times or crashes during peak usage.
- **Mitigation:** Implement caching strategies and optimize database queries for high-traffic scenarios.

## Test Schedule
The test schedule was too big to put into this document, so please see the test_schedule located in our docs folder: `TableReservationSystem/docs`.

## Risks & Issues

### 1. Risks Associated with the Testing Process:
- **Double bookings or incorrect availability:** Users may book tables that are no longer available due to concurrency issues or delayed availability updates.
  - **Mitigation:** Implement database transaction controls and locking mechanisms to prevent race conditions.
- **Failure in SMS/Email notifications:** Messages may not be delivered due to incorrect configurations, third-party service downtime, or invalid user data.
  - **Mitigation:** Implement robust error handling and retries for failed messages. Validate that the user data (email/phone number) is correct during booking.
- **Performance degradation during high load:** The system may slow down or crash during peak periods, affecting the user experience.
  - **Mitigation:** Regular load testing and implementing autoscaling for server resources during high traffic.
- **Delays in confirming bookings:** Confirmation texts or emails may be delayed, leading to customer frustration.
  - **Mitigation:** Test the SMS/Email queue to ensure efficient handling of messages. Use real-time monitoring of message delivery.
- **Missed or unverified edge cases:** There might be edge cases in functionality (e.g., rare booking modification scenarios) that are not covered during testing.
  - **Mitigation:** Use exploratory testing to uncover unexpected behaviors and edge cases.

### 2. Potential System Risks:
- **Data loss during updates:** When users modify or cancel bookings, there may be a risk of data corruption or loss due to database issues.
  - **Mitigation:** Implement data validation checks and transactional rollback mechanisms in case of failure.
- **Security vulnerabilities:** Users may exploit vulnerabilities (e.g., in the waiting list feature or through user inputs).
  - **Mitigation:** Conduct regular security testing, including input validation and sanitization to prevent injection attacks.
- **Inaccurate reporting of table availability:** Delays in syncing between the database and front-end might lead to tables showing as available when they are not.
  - **Mitigation:** Use real-time database updates and optimize communication between the front-end and back-end.

## Conclusion
This test plan provides a structured approach to testing the Table Reservation System by defining the testing approaches, scope, and potential risks. By conducting white-box, functional, and performance testing, we aim to ensure that the system is robust, reliable, and user-friendly. With defined mitigation strategies, we aim to minimize risks and ensure smooth operation during all scenarios.
