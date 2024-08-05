
# Use the official Node.js image as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the React application
RUN npm run build

# Use the official Nginx image to serve the built React application
FROM nginx:alpine

# Copy the built React application from the previous stage to the Nginx html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 to be able to access the application
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
