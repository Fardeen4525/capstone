# capstone
Two sets of specifications have been created for this project. The first set is general and not domain specified. This is for students who want to practice and have their own topic they want to use as the content for the project. Students who may not have their own idea can use the Casting Agency specifications to have slightly more structure when you get started.
Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Models:

Movies with attributes title and release date
Actors with attributes name, age and gender
Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/
Roles:
Casting Assistant
Can view actors and movies
Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies
Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database
Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role
