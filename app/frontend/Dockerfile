FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY src/ ./src
COPY public/ ./public
COPY config-overrides.js ./
COPY tsconfig.json ./

RUN npm run build
CMD ["npm", "start"]