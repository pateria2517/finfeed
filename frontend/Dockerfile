FROM node:20-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS build
ARG NEXT_PUBLIC_API_URL=
ARG INTERNAL_API_URL=http://backend:8000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV INTERNAL_API_URL=${INTERNAL_API_URL}
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
RUN addgroup -S feedz && adduser -S feedz -G feedz
COPY --from=build --chown=feedz:feedz /app/.next/standalone ./
COPY --from=build --chown=feedz:feedz /app/.next/static ./.next/static
USER feedz
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
