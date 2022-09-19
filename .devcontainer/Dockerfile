ARG VARIANT="3.10-bullseye"
FROM python:${VARIANT} as builder

RUN pip install -U pip
RUN pip install pipenv

COPY Pipfile.lock .
RUN PIPENV_VERBOSITY=-1 pipenv requirements --dev --exclude-markers > /requirements-dev.txt

FROM python:${VARIANT}

WORKDIR /workspaces/the_ray_tracer_challenge_py

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -s /bin/bash -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

COPY --from=builder requirements-dev.txt .

ENV PATH="${PATH}:/home/vscode/.local/bin"

RUN pip --no-cache-dir install -U pip
RUN pip --disable-pip-version-check --no-cache-dir install -r requirements-dev.txt





