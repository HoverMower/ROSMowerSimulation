FROM paddycube/rosmower:dev
LABEL maintainer ""

ENV DEBIAN_FRONTEND noninteractive

# Setup your sources list and keys

RUN mkdir /home/ubuntu/catkin_ws/src/rosmower_msgs
RUN mkdir /home/ubuntu/catkin_ws/src/ROSMower
RUN mkdir /home/ubuntu/catkin_ws/src/open_mower_ros
RUN mkdir /home/ubuntu/catkin_ws/src/ftc_local_planner

COPY modules/ROSMower /home/ubuntu/catkin_ws/src/ROSMower
COPY modules/rosmower_msgs /home/ubuntu/catkin_ws/src/rosmower_msgs
COPY modules/open_mower_ros /home/ubuntu/catkin_ws/src/open_mower_os
COPY modules/ftc_local_planner /home/ubuntu/catkin_ws/src/ftc_local_planner

WORKDIR /home/ubuntu/catkin_ws

# build catkin workspace
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/catkin_ws; catkin_make'

