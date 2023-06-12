FROM debian

# Set the working directory
WORKDIR /app

# Update package repositories and install nmap
RUN apt-get update && apt-get install -y nmap

# Copy the entrypoint script to the container
COPY port-entrypoint.sh /app/port-entrypoint.sh

# Set the entrypoint script as executable
RUN chmod +x /app/port-entrypoint.sh

# Specify the entrypoint command
CMD ["/app/port-entrypoint.sh"]