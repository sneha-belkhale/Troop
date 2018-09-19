# Using python3.6 for the parent image
FROM python:3.6
ARG ip_address
ARG foxdot_path
ARG pkg_path

# Install FoxDot
RUN pip install FoxDot

# Modify some foxdot files with user info...
RUN mkdir -p ${pkg_path}
RUN ln -s /usr/local/lib/python3.6/site-packages/FoxDot ${foxdot_path}
RUN sed -i -E s/'localhost'/"${ip_address}"/ /usr/local/lib/python3.6/site-packages/FoxDot/lib/Settings/conf.txt

RUN sed -i -E "s@__file__\ \+\ \"\/\.\.\/\.\.\/\.\.\/\"@\"${foxdot_path}\"@" /usr/local/lib/python3.6/site-packages/FoxDot/lib/Settings/__init__.py
RUN sed -i -E 's/realpath/abspath/' /usr/local/lib/python3.6/site-packages/FoxDot/lib/Settings/__init__.py

# Copy over modified foxdot files
COPY foxdot/OSC3.py /usr/local/lib/python3.6/site-packages/FoxDot/lib/OSC3.py
COPY foxdot/main_lib.py /usr/local/lib/python3.6/site-packages/FoxDot/lib/Code/main_lib.py
COPY foxdot/__main__.py /usr/local/lib/python3.6/site-packages/FoxDot/__main__.py

# Run FoxDot when the container launches
CMD ["python", "-m", "FoxDot", "--socket"]
