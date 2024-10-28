# Server

Server is the entry point for the application. Implemented using Flask and SocketIO for the API and WebSocket.


## Server Config

By default, the server is configured to run in development mode. To run in production mode, set the `SERVER_ENV` environment variable to `production`.

::: spielberg.entrypoint.api.server.LocalAppConfig

::: spielberg.entrypoint.api.server.ProductionAppConfig

## Server Initialization

::: spielberg.entrypoint.api.create_app
