# syntax=docker/dockerfile:1

# ═════════════════════════════════════════════════════════════════════════════
# BASE — Alpine, shared system packages, and non-root user
# ═════════════════════════════════════════════════════════════════════════════
FROM node:24-alpine AS base

# libc6-compat: required by some native Node addons on Alpine
# curl: used by the compose healthcheck
RUN apk add --no-cache libc6-compat curl

WORKDIR /app

# Non-root user — same UID/GID as every other service in the compose stack
RUN addgroup --gid 1001 nodejs && \
    adduser  --uid 1001 --ingroup nodejs --disabled-password nextjs

ENV NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

EXPOSE 3000

# ═════════════════════════════════════════════════════════════════════════════
# DEPS — install node_modules (runs as root so npm can write its cache)
# ═════════════════════════════════════════════════════════════════════════════
FROM base AS deps

COPY package.json package-lock.json* ./
RUN npm ci && chown -R nextjs:nodejs /app

# ═════════════════════════════════════════════════════════════════════════════
# BUILDER — compile the Next.js production bundle
# ═════════════════════════════════════════════════════════════════════════════
FROM deps AS builder

COPY --chown=nextjs:nodejs . .
USER nextjs

ARG NEXT_PUBLIC_API_BASE_URL=http://localhost/iam/v1
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

RUN npm run build

# ═════════════════════════════════════════════════════════════════════════════
# PRODUCTION — minimal runtime (node_modules + .next output only)
# ═════════════════════════════════════════════════════════════════════════════
FROM base AS production

COPY --from=deps    --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/.next        ./.next
COPY --chown=nextjs:nodejs package.json ./

USER nextjs

ENV NODE_ENV=production

CMD ["npm", "run", "start"]

# ═════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT — hot-reload dev server; source bind-mounted by docker-compose
# ═════════════════════════════════════════════════════════════════════════════
FROM deps AS development

COPY --chown=nextjs:nodejs . .
USER nextjs

ENV NODE_ENV=development

CMD ["npm", "run", "dev"]
