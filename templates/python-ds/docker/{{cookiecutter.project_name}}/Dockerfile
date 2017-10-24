FROM continuumio/miniconda3:latest

# Ensure Base image is up to date
RUN conda update -y conda \
        && conda install conda-build \
        && conda clean --all

# Install Frozen Package Dependencies
ADD frozen_environment.yml frozen_environment.yml

RUN conda env update -n root -f frozen_environment.yml \
        && conda uninstall --force -y qt pyqt \
        && conda clean --all
