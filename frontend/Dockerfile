FROM node:20 AS builder

WORKDIR /app
COPY package.json ./
COPY yarn.lock* package-lock.json* ./
RUN yarn install --frozen-lockfile || npm install
COPY . .
RUN yarn build || npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
