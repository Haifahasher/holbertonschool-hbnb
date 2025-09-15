**Objective**
*Secure various API endpoints to allow only authenticated users to perform specific actions, including creating and modifying places and reviews, as well as updating their own user details. Access will be controlled via JWT authentication, with additional validation to ensure users can only modify data that belongs to them (e.g., places they own, reviews they created).*

**Context**
*Authenticated user access is a critical part of securing an API. By ensuring that only authorized users can perform specific actions, the integrity of the data is protected. This task focuses on securing endpoints related to creating and modifying places and reviews, while also allowing users to modify their own data.

In this task, you will:

Secure endpoints to ensure only authenticated users can create, update, and delete resources.
Add logic to validate ownership of places and reviews.
Implement logic to prevent users from reviewing places they own or reviewing a place multiple times.
Verify that public users can access the PUBLIC endpoints without a JWT token.*
