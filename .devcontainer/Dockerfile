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
                       
RUN apt-get upgrade -y   # safer than dist-upgrade

# Optional: Create venv instead of system packages
# RUN python3 -m venv /ros_env
# RUN /ros_env/bin/pip install --upgrade pip gym transforms3d

# RUN python3 -m pip install --break-system-packages gym transforms3d
COPY requirements.txt /requirements.txt
RUN pip install --break-system-packages --no-deps -r /requirements.txt

WORKDIR /ros_ws/src
COPY packages.repos .

# Import repositories + dep install + build
RUN vcs import < packages.repos && \
    cd /ros_ws && \
    apt-get update && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build

# Copy your own package and rebuild
COPY . /ros_ws/src/f1tenth_gym_ros
RUN cd /ros_ws && \
    apt-get update --fix-missing && \
    rosdep install -i --from-path src --rosdistro jazzy -y && \
    source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build
