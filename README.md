
git config --local user.name "Александр Шалин"
git config --local user.email "shalunbdk@gmail.com"

docker network create myNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=gerjgnladasfeet \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image

docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking_nginx \
    -v ./nginx.conf:/etc/nginx/nginx.conf \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -v /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=myNetwork \
    -d -p 443:443 nginx

    docker run --name booking_nginx -v ./nginx.conf:/etc/nginx/nginx.conf --network=myNetwork --rm -p 80:80 nginx

docker build -t booking_image .

