FROM node:22-alpine
WORKDIR /app
COPY evalloop.mjs .
ENV NODE_ENV=production PORT=8080 DATA_DIR=/data COOKIE_SECURE=1 TRUST_PROXY=1
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://127.0.0.1:8080/health || exit 1
CMD ["node", "evalloop.mjs"]
