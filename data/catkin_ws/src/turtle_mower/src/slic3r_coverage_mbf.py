#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Polygon,Point32
from slic3r_coverage_planner.srv import PlanPath
from mbf_msgs.msg import *
from nav_msgs.msg import Path
from std_msgs.msg import Header
import actionlib

# Example of how to call slic3r_coverage_planner PlanPath service.
# It takes a polyon as outline and an arary of polygones for inner holes (isles)
# It returns a list of Slic3r pathes. Each Slic3r path object consists of a nav_msgs/Path object
#
# This program calls the Slic3r path planner for a simple polygon and send the result to move_base_flex

def client():
    rospy.init_node('talker', anonymous=True)
    rospy.loginfo("Wait for Slic3r service")
    rospy.wait_for_service('slic3r_coverage_planner/plan_path')
    mbf_client = actionlib.SimpleActionClient("move_base_flex/exe_path", ExePathAction )
    rospy.loginfo("wait for MBF Action server")
    #mbf_client.wait_for_server()


    while not mbf_client.wait_for_server(rospy.Duration(5)):
        rospy.loginfo(" Waiting for Move Base")
    

    try:
        slic3r_proxy = rospy.ServiceProxy('slic3r_coverage_planner/plan_path', PlanPath)
        pathSrv = PlanPath()
        pathSrv.angle = 20
        pathSrv.outline_count = 2
        p = Polygon() # outline
        holes= []
        hole = Polygon()
        hole.points = [
            Point32(x=2, y=1),
            Point32(x=-2, y=1),
            Point32(x=-2, y=0),
            Point32(x=-1, y=1),
            Point32(x=2, y=2),]
        holes.append(hole)  
        p.points = [
            Point32(x=0, y=5),
            Point32(x=4, y=4),
            Point32(x=4, y=1),
            Point32(x=3, y=-2),
            Point32(x=1, y=-3),
            Point32(x=-2, y=0),
            Point32(x=-3, y=-1.3),
            Point32(x=-4, y=-4),
            Point32(x=-3, y=-2),
            Point32(x=-2, y=-1),
            Point32(x=-1, y=3),
            Point32(x=0, y=5)]
        #p.points = [Point32(x=1.0, y=1.0),
        #            Point32(x=-1.0, y=1.0),
        #            Point32(x=-1.0, y=-1.0),
        #            Point32(x=1.0, y=-1.0),
        #            Point32(x=1.0, y=1.0)]
        #p.points = [Point32(x=-0.1, y=1.8),
        #            Point32(x=-1.2, y=0.5),
        #            Point32(x=-1.8, y=0.0),
        #            Point32(x=-1.6, y=-0.5),
        #            Point32(x=1.0, y=-1.0),
        #            Point32(x=1.1, y=-0.6),
        #            Point32(x=1.8, y=0.0),
        #            Point32(x=1.6, y=0.6),
        #            Point32(x=0.1, y=1.5),
        #            Point32(x=0.3, y=1.7),
        #            Point32(x=-1.1, y=1.8)]                    
        pathSrv.outline = p
        
        pathSrv.fill_type = 0 # linear
        #['fill_type', 'angle', 'distance', 'outer_offset', 'outline_count', 'outline', 'holes']
        resp1 = slic3r_proxy(0, 20.0, 0.2, 0, 3, p, holes) 
        nav_path = Path()
        header = Header()
        rate = rospy.Rate(1) # 1hz

        while not rospy.is_shutdown(): 

            # prepare nav_msgs/Path message
            header.frame_id = "odom"
            header.stamp = rospy.Time.now()
            nav_path.header = header
            nav_path.poses = resp1.paths[0].path.poses
              
            # prepare mbf_action
            mbf_path = ExePathGoal()
            mbf_path.controller = "FTCPlanner"
            mbf_path.path = nav_path

            # send goal
            mbf_client.send_goal(mbf_path)
            rospy.spin() # infinite loop ensures to send only once
      
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == '__main__':
    try:
        client()
    except rospy.ROSInterruptException:
        pass