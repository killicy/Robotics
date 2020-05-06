#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
def mover():

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('moveturtlefwd')
    
    curve = Twist()
    curve.linear.x = .9
    curve.angular.z = 0.0
    rate=rospy.Rate(15)
    change_time=rospy.Time.now()
    change_time2=rospy.Time.now()
    turning=False
     
    while not rospy.is_shutdown():
      
        pub.publish(curve)
    
        if (rospy.Time.now() - change_time) < rospy.Duration(4):
            curve.angular.z = 0
            curve.linear.x =.1

        elif rospy.Time.now() - change_time < rospy.Duration(9.27):
            curve.linear.x = 0.0
            curve.angular.z = .3

        if rospy.Time.now() - change_time > rospy.Duration(9.27):
            change_time = rospy.Time.now()

if __name__ == '__main__':
    try:
        mover()
    except rospy.ROSInterruptException:
        pass
