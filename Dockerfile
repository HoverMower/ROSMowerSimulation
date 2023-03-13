FROM paddycube/rosmower:dev
LABEL maintainer ""

ENV DEBIAN_FRONTEND noninteractive

# Setup your sources list and keys

RUN cd /home/ubuntu/catkin_ws/src
RUN git clone https://github.com/HoverMower/Slic3r
RUN git clone https://github.com/HoverMower/slic3r_coverage_planner
RUN git clone https://github.com/HoverMower/rosmower_msgs
RUN git clone https://github.com/HoverMower/ROSMower
RUN git clone https://github.com/HoverMower/open_mower_ros

WORKDIR /home/ubuntu/catkin_ws

# build catkin workspace
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/catkin_ws; catkin_make'

