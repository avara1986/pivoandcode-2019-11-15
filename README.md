#Install

```bash
docker-compose up
```
Open http://127.0.0.1:8081/

See traces: http://localhost:16686/



# Create the docker images:
```bash
docker build -t chat_db:v1 -f chat_db/Dockerfile chat_db/
docker build -t chat_svc:v1 -f chat_svc/Dockerfile chat_svc/
docker build -t chat_front:v1 -f chat_front/Dockerfile chat_front/
```