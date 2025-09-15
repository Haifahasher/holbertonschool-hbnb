**Objective**
*Set up JWT-based authentication for the HBnB application, enabling secure login functionality. This task involves configuring the API to generate and verify JWT tokens using the flask-jwt-extended extension. Tokens will be issued upon successful login and required for accessing protected endpoints.*

**Context**
*JWT (JSON Web Token) allows secure authentication by providing a token that clients can use to access protected resources without having to re-authenticate on every request. JWT is stateless, meaning the server doesn't need to store user sessions, making it ideal for scalable applications. JWT tokens also allow embedding additional claims (such as user roles), which is useful for authorization.

In this task, we will set up user login, issue JWT tokens, and use these tokens to protect specific API endpoints.*
