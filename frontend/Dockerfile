# Step 1: Build React app
FROM node:16-slim as build

WORKDIR /app

COPY package.json ./
RUN npm install
COPY . ./
RUN npm run build

# Step 2: Serve React app with Nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
