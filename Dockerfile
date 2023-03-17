FROM paddycube/rosmower:dev
LABEL maintainer ""

ENV DEBIAN_FRONTEND noninteractive

# Setup your sources list and keys

RUN mkdir -p /home/ubuntu/catkin_ws/src/rosmower_msgs
RUN mkdir -p /home/ubuntu/catkin_ws/src/ROSMower
RUN mkdir -p /home/ubuntu/catkin_ws/src/oled_display_node
RUN mkdir -p /home/ubuntu/catkin_ws/src/ftc_local_planner
RUN mkdir -p /home/ubuntu/catkin_ws/src/Slic3r
RUN mkdir -p /home/ubuntu/catkin_ws/src/slic3r_coverage_planner
RUN mkdir -p /home/ubuntu/catkin_ws/src/ds4_driver
RUN mkdir -p /home/ubuntu/.ds4drv

# ublox installation
RUN apt-get install -y ros-melodic-ublox

#DS4 controller
COPY modules/ds4_driver /home/ubuntu/catkin_ws/src/ds4_driver
COPY modules/ds4drv /home/ubuntu/.ds4drv
RUN apt-get install -y python3-setuptools
RUN cd /home/ubuntu/.ds4drv
RUN mkdir -p /home/ubuntu/.local/lib/python3.6/site-packages
WORKDIR /home/ubuntu/.ds4drv
RUN python3 setup.py install --prefix /home/ubuntu/.local
RUN cp udev/50-ds4drv.rules /etc/udev/rules.d/
#RUN udevadm control --reload-rules
#RUN udevadm trigger
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/catkin_ws; catkin_make'

# Slic3r coverage planner
COPY modules/Slic3r /home/ubuntu/catkin_ws/src/Slic3r
COPY modules/slic3r_coverage_planner /home/ubuntu/catkin_ws/src/slic3r_coverage_planner
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/catkin_ws; catkin_make'

# others
COPY modules/ROSMower /home/ubuntu/catkin_ws/src/ROSMower
COPY modules/rosmower_msgs /home/ubuntu/catkin_ws/src/rosmower_msgs
COPY modules/ftc_local_planner /home/ubuntu/catkin_ws/src/ftc_local_planner
COPY modules/oled_display_node /home/ubuntu/catkin_ws/src/oled_display_node
COPY modules/ds4_driver /home/ubuntu/catkin_ws/src/ds4_driver
RUN chmod -R 777 .

WORKDIR /home/ubuntu/catkin_ws

# build catkin workspace
#RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/catkin_ws; catkin_make'

