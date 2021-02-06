## Please note: the default `develop` branch does not house the full app, but the BE to another front-end. Use `master` branch for the full app where the local run instructions will work.
# Chat Room App

This app uses 
- Python FastAPI+WebSockets [docs](https://fastapi.tiangolo.com/)
- MotorAsyncIO [docs](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)
- MongoDB [docs](https://docs.mongodb.com/manual/)


## To Run Locally

I've set it up so that you only need to use the `run` script

```
$ ./run
```

Then go to `localhost:8000/{room_name}/{user_name}`

The room_name and user_name can be replaced by whatever you want (although you need to match room_names to actually chat with friends)

## Description 

The front-end is simple HTML/CSS and Javascript using the WebSocket connection to establish a client server connection. 
Currently (05-04-2020) this works perfectly on it's own but there is no persistence to the database so chat sessions and usernames cannot be stored.

The back-end has been partially written and yet to be connected with the backend. 
A few more instructions need to be present in order to maintain persistence.
So with MongoDB we are storing a Username/Password combo, all of the active rooms, and all of the messages per room.
When connected to the front-end the UX/UI will drastically change as we can display all active chat rooms to join as well as the members inside of a chatroom.


UPDATE: 1/26/2021
I will be starting work on a React Front End with the hopes of building a fully functioning web app instead of just a POC.
The backend work for that will be continued on the `full_platform` branch.
