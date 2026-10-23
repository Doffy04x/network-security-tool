FROM python:3.12-alpine@sha256:b658b05ce9c4eb97ec6fc19424818a1f31993659c2b505a532f470e83807815d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk upgrade --no-cache \
    && addgroup -g 10001 app \
    && adduser -D -H -u 10001 -G app app \
    && python -m pip uninstall -y pip

WORKDIR /app
COPY --chown=10001:10001 network_check.py ./network_check.py
COPY --chown=10001:10001 api/ ./api/

USER 10001:10001
EXPOSE 8000
CMD ["python", "-m", "api.server"]
