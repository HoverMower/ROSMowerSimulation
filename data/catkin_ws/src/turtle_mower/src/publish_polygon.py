#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Polygon, PolygonStamped, Point32
from std_msgs.msg import Header

def talker():
    pub = rospy.Publisher('polygon', PolygonStamped, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
            p = PolygonStamped()
            header = Header()
            header.frame_id = "map"
            header.stamp = rospy.Time.now()
            p.header = header
            p.polygon.points = [Point32(x=1.0, y=1.0),
                                Point32(x=-1.0, y=1.0),
                                Point32(x=-1.0, y=-1.0),
                                Point32(x=1.0, y=-1.0)]
            pub.publish(p)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass