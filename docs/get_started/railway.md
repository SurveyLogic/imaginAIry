!!! note

    Director will soon be available on the Railway Marketplace for easy deployment.

## Deployment Instructions via Railway CLI

1. Clone the Director repository to your local machine:
    ```
    git clone https://github.com/video-db/Director
    ```
2. Change the directory to the cloned repository:
    ```
    cd Director
    ```
3. Install the [Railway CLI](https://docs.railway.app/guides/cli).
4. Navigate to the Railway [Dashboard](https://railway.app/dashboard) and create an empty project.
5. Add two empty services to the project, and rename them as backend and frontend.
6. Log in to Railway via the CLI:
    ```
    railway login
    ```

### Deploy the backend service:

* Navigate to the backend service directory
* Link your project and the backend service
    ```
    railway link 
    ```
* Deploy the backend service
    ```
    railway up
    ```
    
### Deploy the frontend service:

* Navigate to the frontend service directory
* Link your project and the frontend service
    ```
    railway link 
    ```
* Deploy the frontend service
    ```
    railway up
    ```

### Backend Configuration
* After deployment, go to the [Railway project dashboard](https://railway.app/dashboard), and under the backend service, update the environment variables:
    ``` 
    VIDEO_DB_API_KEY="your_video_db_api_key"
    OPENAI_API_KEY="your_openai_api_key"
    ```

* Go to Settings → Networking → Public Networking, generate a domain, and copy the domain. You will need to use this domain in the frontend service configuration.


### Frontend Configuration
* In the frontend service , update the following environment variable:
    ```
    VITE_APP_BACKEND_URL="deployed_backend_service_public_url"
    ```

* After deployment, generate a domain and navigate to the frontend service URL (which can be found in Settings → Networking → Public Networking) in your web browser to access the Director application.
