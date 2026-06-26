ARG NODE_VERSION=24.14.0-alpine

FROM node:${NODE_VERSION}

ENV PNPM_HOME="/pnpm" \
    PATH="/pnpm:$PATH"

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml ./

RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile

EXPOSE 5173

CMD ["pnpm", "dev", "--host"]
