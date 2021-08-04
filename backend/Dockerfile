FROM node:14

WORKDIR /usr/src/Jewelify_project

COPY package.json ./
COPY yarn.lock ./
RUN yarn
COPY ./ ./
RUN chmod +x /usr/src/Jewelify_project/wait-for-it.sh
