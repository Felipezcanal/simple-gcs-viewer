# Choose the Image which has Node installed already
FROM node:lts-alpine

ARG VITE_BASE_GCS_PATH
ARG VITE_API_URL

ENV VITE_BASE_GCS_PATH=$VITE_BASE_GCS_PATH
ENV VITE_API_URL=$VITE_API_URL

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

EXPOSE 80
CMD [ "http-server", "dist", "-p", "80" ]