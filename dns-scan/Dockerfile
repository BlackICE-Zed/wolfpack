FROM kalilinux/kali-rolling

# Set the working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y ffuf seclists

# Copy the entrypoint script to the container
COPY dns-entrypoint.sh /app/dns-entrypoint.sh

# Set the entrypoint script as executable
RUN chmod +x /app/dns-entrypoint.sh

# Specify the entrypoint command
CMD ["/app/dns-entrypoint.sh"]