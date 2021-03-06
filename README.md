Problem:  
1. Upload csv file containing work history of employees.  
2. Generate biweekly aggregated report.  

A bit about the app: The app is done up with Python, Django, Postgres, Redis with Docker containers.
I have Celery workers running in the worker container which picks up the records that need to be processed, and updates the Postgres db asynchronously in the background. This enables speedy responses to the user. I am excited about the backend architecture. I am also excited about the docker containers, because this provides the same replicable platform to keep iterating on this app no matter what their host OS is. Docker containers also enable us to better package our app for production level deployments.

The app will run on either a Mac or a Linux and NEEDS to have docker installed.

PREREQUISITE: Have docker installed.


Onwards, to START the app:  
1. Go to a terminal, navigate into the toplevel folder containing the Makefile.  
2. Run: make build  
3. Run: make dev  
4. It'll take some time for containers to come up. After about 15 seconds or so, in your browser go to: 127.0.0.1:8000  
5. You can now use the app to upload a file, and check for reports.  

Note: Initially, I had imagined I was going to separate out the backend and frontend concerns into their own
separate containers. I had started off with the "backend" folder for the backend service. Eventually, I dropped my idea of building a React app for the frontend, and bundled the js in django templates. I prefer working on the backend mostly.

Let me know if you have any questions.

Cheers,
Druhin.  


Troubleshooting:
1. When you first hit 127.0.0.1:8000, and it errors out saying it could not find fields in the DB, chances are
the Postgres container did not come up in time for the migrations to occur. In such a case, stop the
containers, and run a make dev. This should apply the migrations now, since the Postgres container hopefully already has been pulled and exists.
