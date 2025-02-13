# Stage 1: Build
FROM node:16-alpine as build

WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Nginx
FROM nginx:stable-alpine
COPY --from=build /frontend/build /usr/share/nginx/html

# Copy your custom nginx.conf that listens on 8080
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
