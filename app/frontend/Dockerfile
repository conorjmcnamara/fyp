FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY src/ ./src
COPY public/ ./public
COPY tsconfig.json ./

RUN npm run build

EXPOSE ${FRONTEND_PORT}
CMD PORT=${FRONTEND_PORT} npm start