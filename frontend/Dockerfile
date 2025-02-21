FROM node:18.20-alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

EXPOSE 4200
RUN npm install -g @angular/cli@16.2.16

RUN npm install

CMD ["ng", "serve", "--host", "0.0.0.0"]