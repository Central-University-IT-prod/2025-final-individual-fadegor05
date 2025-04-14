docker compose down
docker container rm solution-postgres-1
docker volume rm solution_postgres_data
docker compose up --build
