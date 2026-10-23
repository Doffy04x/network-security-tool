# Initial container setup for the TP 3 comparison, before hardening.
FROM python:3.12-bookworm@sha256:14a4933e6cef421424f7a66d89a3f4eafcbd0d90e0a822251f298e05132dc735

WORKDIR /app
COPY network_check.py ./network_check.py
COPY api/ ./api/
EXPOSE 8000
CMD ["python", "-m", "api.server"]
