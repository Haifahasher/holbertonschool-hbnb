**Objective**
*Restrict access to specific API endpoints so that only users with administrative privileges can perform certain actions. These actions include creating new users, modifying any user's details (including email and password), and adding or modifying amenities. Additionally, administrators can perform the same tasks as authenticated users without being restricted by ownership of places and reviews.*

**Context**
*Role-based access control (RBAC) is crucial in API security. Administrators have the highest level of privileges, and this task will allow them to bypass restrictions that regular users face. This includes the ability to manage any user or resource in the system.

In this task, you will:

Implement logic for restricting access to specific endpoints based on the user's role (is_admin).
Ensure that administrators can manage user accounts, including creating and modifying user details.
Allow administrators to bypass ownership restrictions for places and reviews.*
