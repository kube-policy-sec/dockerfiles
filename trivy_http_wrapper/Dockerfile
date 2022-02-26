FROM docker.io/alpine:3.15.0

RUN apk --no-cache add ca-certificates git python3
COPY trivy /usr/local/bin/trivy
COPY trivy_repo/contrib/*.tpl contrib/
COPY trivy_web.py trivy_web.py


ENTRYPOINT ["python3", "trivy_web.py"]


