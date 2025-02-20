# ProPresenter message client v1.0.0
![REST API Executor Server](assets/api-rest-log.png "REST API Executor Server")

## **1. How to Start the Docker Container**

### **Build and Start the Containers**

To build and start the API server and Nginx reverse proxy, use the following command:

```bash
docker-compose up --build -d
```

This command:
- Builds the necessary Docker images.
- Starts the containers in detached mode (`-d`).

### **Check Running Containers**

To verify that the containers are running, execute:

```bash
docker ps
```

### **Stop the Containers**

To stop the running containers, use:

```bash
docker-compose down
```

This will shut down and remove the containers.

### **Restart the Containers**

If the containers are already built and you want to restart them:

```bash
docker-compose up -d
```

### **View Logs**

To check the logs of the running API server:

```bash
docker logs -f propresenter_message_client
```
