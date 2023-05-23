# Use the official Redis image as the base image
FROM redis:latest

# Copy the Redis configuration file into the Docker container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Start Redis with the custom configuration file
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf"]
