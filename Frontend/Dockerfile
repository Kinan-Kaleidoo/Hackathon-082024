# Use an official Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Define environment variable for the production build
ENV NODE_ENV=production

# Set the environment variable to fix the OpenSSL issue
ENV NODE_OPTIONS=--openssl-legacy-provider

# Print Node.js and npm versions
RUN node -v && npm -v

# Build the React app
RUN npm run build

# Install serve to serve the production build
RUN npm install -g serve

# Command to run the application
CMD ["serve", "-s", "build"]
