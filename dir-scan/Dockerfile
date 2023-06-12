FROM kalilinux/kali-rolling

# Set the working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt -y install wfuzz seclists

# Copy the entrypoint script to the container
COPY dir-entrypoint.sh /app/dir-entrypoint.sh

# Set the entrypoint script as executable
RUN chmod +x /app/dir-entrypoint.sh

# Specify the entrypoint command
CMD ["/app/dir-entrypoint.sh"]