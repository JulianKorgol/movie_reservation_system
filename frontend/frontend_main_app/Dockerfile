FROM node:24-alpine

RUN apk add --no-cache libc6-compat

WORKDIR /app

# Non-root user — same UID as prod so volume permissions match
RUN addgroup --gid 1001 nodejs && \
    adduser  --uid 1001 --ingroup nodejs --disabled-password nextjs

# Install deps as root, then hand ownership to nextjs
COPY package.json package-lock.json* ./
RUN npm ci

# Give the user ownership of the working dir
RUN chown -R nextjs:nodejs /app

USER nextjs

ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000

EXPOSE 3000

# Overridden by docker-compose.dev.yml command: npm run dev
CMD ["npm", "run", "dev"]
