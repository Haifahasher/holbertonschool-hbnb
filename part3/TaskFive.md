**Objective**
*Replace the in-memory repository with a SQLAlchemy-based repository for persistence. In this task, you will create the SQLAlchemyRepository and integrate it into the project for managing database interactions. This task will lay the foundation for further model mapping and database setup in subsequent tasks.*

**Context**
*In the previous parts of the project, the persistence layer was managed using an in-memory repository. This task introduces SQLAlchemy to persist data in an SQLite database during development, preparing the application for a production-ready relational database. The repository pattern remains the same, but the implementation will now interact with SQLAlchemy for all CRUD operations. Due to the fact that the database has not yet been initialized, this task focuses only on creating the repository. Model mapping and database initialization will follow in the next task.

You will:

Create the SQLAlchemy repository that implements the existing repository interface.
Refactor the existing Facade to utilize the SQLAlchemy-based repository for user operations.
Provide code and detailed instructions for integration, but no database initialization will be performed yet.*
