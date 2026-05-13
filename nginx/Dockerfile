# syntax=docker/dockerfile:1
FROM nginx:stable-alpine

# ── Non-root user (UID/GID 1001 matches every other service) ─────────────────
RUN addgroup -g 1001 appgroup && \
    adduser  -u 1001 -G appgroup -D appuser

# Fix ownership so appuser can read config and write log symlinks.
# /var/log/nginx/* are already symlinked → /dev/stdout & /dev/stderr
# in the official image, so no actual file writes happen there.
# /var/cache/nginx and /var/run are mounted as tmpfs by docker-compose.
RUN chown -R appuser:appgroup \
        /etc/nginx/conf.d \
        /var/log/nginx

# ── Config ────────────────────────────────────────────────────────────────────
COPY nginx.conf  /etc/nginx/nginx.conf
COPY conf.d/     /etc/nginx/conf.d/

USER appuser

EXPOSE 80

# "daemon off" keeps nginx in the foreground so Docker can manage the process.
CMD ["nginx", "-g", "daemon off;"]
