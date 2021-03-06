# Udacity Full Stack Development capstone project.
## Casting Agency Specifications:<br>
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:<br>
* Movies
  * title 
  * release date<br>
* Actors 
  * name
  * age
  * gender<br>
### Endpoints:<br>
* GET /actors and /movies<br>
* DELETE /actors/ and /movies/<br>
* POST /actors and /movies and<br>
* PATCH /actors/ and /movies/<br>
### Roles:<br>
* Casting Assistant<br>
  * Can view actors and movies<br>
* Casting Director<br>
  * All permissions a Casting Assistant has and…<br>
  * Add or delete an actor from the database<br>
  * Modify actors or movies<br>
* Executive Producer<br>
  * All permissions a Casting Director has and…<br>
  * Add or delete a movie from the database<br>
### Tests:<br>
* One test for success behavior of each endpoint<br>
* One test for error behavior of each endpoint<br>
* At least two tests of RBAC for each role<br>
