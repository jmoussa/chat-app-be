### Please note: this default `develop` branch does not house the full app, but the BE to another front-end. 
#### Use `master` branch for the full app where the POC will work.

# Chat Room App

This API was built to support the [chat_app_FE](https://github.com/jmoussa/chat_app_FE).
In the `/api` folder you will find the routes for rooms and users. 
This being a FastAPI app, you will also be able to get quick documenatation on the routes and request types after running.

This app uses: 

- Anaconda (for Python environemnt management)
- Python FastAPI+WebSockets [docs](https://fastapi.tiangolo.com/)
- Pymongo[docs](https://pymongo.readthedocs.io/en/stable/)
- MongoDB [docs](https://docs.mongodb.com/manual/)


## Setting up and running 

I've set it up so that you only need to use the `run` script

```
> conda env create -f environment.yml
> conda activate
> ./run
```

_For quick API documentation, navigate to `localhost:8000/docs` after starting the server_ 

