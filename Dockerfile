FROM python:3.5 AS build
RUN python3 -m venv /venv

ADD requirements.txt /
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

ADD . /invex
RUN /venv/bin/pip install --no-cache-dir /invex

WORKDIR /invex

# Run tests
ADD requirements.txt test-requirements.txt /
RUN python3 -m venv /venv-test && \
          /venv-test/bin/pip install tox==2.9.1 && \
          /venv-test/bin/tox  &&  \
          rm -rf /venv-test

FROM python:3.5-slim AS production

COPY --from=build /venv /venv

ENTRYPOINT ["/venv/bin/invex"]