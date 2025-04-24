# Base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy .env file (if present) and the rest of the application code
COPY . .

# Build the React app with environment variables
ARG REACT_APP_API_URL=http://127.0.0.1:8000/predict
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# Install serve globally to serve the build folder
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]