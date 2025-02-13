# Stage 1: Build
FROM node:16-alpine as build

WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Nginx
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
