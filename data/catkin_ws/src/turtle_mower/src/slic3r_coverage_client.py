#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Polygon,Point32
from slic3r_coverage_planner.srv import PlanPath
from nav_msgs.msg import Path
from std_msgs.msg import Header

# Example of how to call slic3r_coverage_planner PlanPath service.
# It takes a polyon as outline and an arary of polygones for inner holes (isles)
# It returns a list of Slic3r pathes. Each Slic3r path object consists of a nav_msgs/Path object
#
# This program calls the Slic3r path planner for a simple polygon and publishes the first
# path segment as nav_msgs/Path

def client():
    rospy.wait_for_service('slic3r_coverage_planner/plan_path')
    pub = rospy.Publisher('slic3r_path', Path, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    try:
        slic3r_proxy = rospy.ServiceProxy('slic3r_coverage_planner/plan_path', PlanPath)
        pathSrv = PlanPath()
        pathSrv.angle = 20
        pathSrv.outline_count = 2
        p = Polygon() # outline
        holes = []
        p.points = [Point32(x=1.0, y=1.0),
                    Point32(x=-1.0, y=1.0),
                    Point32(x=-1.0, y=-1.0),
                    Point32(x=1.0, y=-1.0)]
        pathSrv.outline = p
        
        pathSrv.fill_type = 0 # linear
        #['fill_type', 'angle', 'distance', 'outer_offset', 'outline_count', 'outline', 'holes']
        resp1 = slic3r_proxy(0, 20, 0.5, 0, 3, p, holes) 
        nav_path = Path()
        header = Header()
        rate = rospy.Rate(1) # 1hz
        while not rospy.is_shutdown(): 
            # wait for subscribers
            connections = pub.get_num_connections()
            # at least one subscriber? send the generated path
            if connections > 0:
                header.frame_id = "map"
                header.stamp = rospy.Time.now()

                nav_path.header = header
                nav_path.poses = resp1.paths[0].path.poses
                pub.publish(nav_path)
                rospy.spin() # infinite loop ensures to send only once
            rate.sleep()
      
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == '__main__':
    try:
        client()
    except rospy.ROSInterruptException:
        pass