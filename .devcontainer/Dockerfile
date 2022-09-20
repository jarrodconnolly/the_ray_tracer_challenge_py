ARG VARIANT="3.10.7-bullseye"
FROM python:${VARIANT}

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID



RUN pip install -U pip
RUN pip install -U pipenv

COPY Pipfile.lock .
RUN PIPENV_VERBOSITY=-1 pipenv requirements --dev --exclude-markers > /tmp/requirements-dev.txt

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -s /bin/bash -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

WORKDIR /workspaces/the_ray_tracer_challenge_py

ENV PATH="${PATH}:/home/vscode/.local/bin"

RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-dev.txt
