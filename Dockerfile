FROM python:3.8.10 AS builder
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
RUN python -m build

FROM python:3.8.10-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY --from=builder /src/dist/* ./
RUN pip install *.tar.gz
VOLUME [ "/target" ]
ENTRYPOINT premiumizeme-sync --folder_id ${FOLDER_ID} /target