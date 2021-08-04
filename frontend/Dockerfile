FROM node:14

WORKDIR /usr/src/Jewelify_project_frontend/

COPY ./package.json ./
COPY ./yarn.lock ./

RUN yarn

COPY ./ ./

CMD yarn start
