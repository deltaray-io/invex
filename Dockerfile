FROM python:3.5 AS build
ARG SKIP_TEST
RUN python3 -m venv /venv

ADD requirements.txt /
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

# XXX: --no-cache-dir is required during pip install
# to resolve the following error:
# AttributeError: module 'bottleneck' has no attribute 'nanmean'
# ...
# ImportError: No module named 'numpy.core._multiarray_umath'
ADD . /invex
RUN /venv/bin/pip install --no-cache-dir /invex

WORKDIR /invex

# Run tests
ADD requirements.txt test-requirements.txt /
RUN if [ $SKIP_TEST != "true" ]; then \
        python3 -m venv /venv-test && \
        /venv-test/bin/pip install tox==2.9.1 && \
        /venv-test/bin/tox  &&  \
        rm -rf /venv-test; \
    fi

FROM python:3.5-slim AS production

COPY --from=build /venv /venv

ENTRYPOINT ["/venv/bin/invex"]
