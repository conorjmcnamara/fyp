# Stage 1: Build application
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY src/ ./src
COPY public/ ./public
COPY --chown=node:node .env ./.env
COPY config-overrides.js postcss.config.js tailwind.config.js tsconfig.json ./

RUN npm run build

# Stage 2: Final runtime image
FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/build /app/build
RUN npm install -g --omit=dev serve

CMD ["sh", "-c", "serve -s build -p $FRONTEND_PORT"]