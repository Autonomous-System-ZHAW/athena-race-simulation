FROM ros:jazzy

SHELL ["/bin/bash", "-c"]

# System dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y git nano vim python3-venv libeigen3-dev tmux \
                       python3-pip \
                       ros-jazzy-rviz2 \
                       ros-jazzy-ackermann-msgs \
                       ros-jazzy-nav2-lifecycle-manager \
                       ros-jazzy-xacro \
                       ros-jazzy-nav2-map-server && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get -y dist-upgrade

# Create a virtual environment for Python packages
# RUN python3 -m venv /opt/ros_env

# Upgrade pip inside venv and install gym
# RUN /opt/ros_env/bin/pip install --upgrade pip && \
#    /opt/ros_env/bin/pip install gym

RUN python3 -m pip install --break-system-packages gym 
RUN python3 -m pip install --break-system-packages transforms3d

# ros2 gym bridge
RUN mkdir -p sim_ws/src/f1tenth_gym_ros
COPY . /sim_ws/src/f1tenth_gym_ros
RUN source /opt/ros/jazzy/setup.bash && \
    cd sim_ws/ && \
    apt-get update --fix-missing && \
    rosdep install -i --from-path src --rosdistro jazzy -y && \
    colcon build

WORKDIR '/sim_ws'
ENTRYPOINT ["/bin/bash"]