# First stage
FROM python:3.8-slim AS builder

RUN mkdir /install
WORKDIR /install

RUN apt-get update \
    && apt-get install make \
    && pip install pipenv
COPY Pipfile* ./

# RUN pipenv lock -r > requirements.txt \
#     && pip install --prefix=/install --ignore-installed -r requirements.txt


# Second unnamed stage
FROM python:3.8-slim

RUN mkdir /home/urbox

RUN adduser urbox
WORKDIR /home/urbox

RUN apt-get update && apt-get install make
RUN pip install pipenv
COPY --from=builder /install /usr/local
COPY ./ ./
RUN make install

#USER urbox