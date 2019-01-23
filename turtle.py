#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

PI = 3.1415926535897


def turtle():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # We wont use Angular component's for the y-axis movement
    vel_msg.linear.x = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.z = 0
    # Receiveing the user's input
    speed = 1  # speed degrees/sec 
    distance = 3
    isForward = True
    vel_msg.linear.y = abs(speed)

    while not rospy.is_shutdown():

        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        # Loop to move the turtle in an specified distance
        while (current_distance < distance):
            # Publish the velocity
            velocity_publisher.publish(vel_msg)
            # Takes actual time to velocity calculus
            t1 = rospy.Time.now().to_sec()
            # Calculates distancePoseStamped
            current_distance = speed * (t1 - t0)
        # After the loop, stops the robot
        vel_msg.linear.y = 0
        # Force the robot to stop
        velocity_publisher.publish(vel_msg)

    angle = 145
    angular_speed = speed * 2 * PI / 360
    relative_angle = angle * 2 * PI / 360
    vel_msg.angular.y = -abs(angular_speed)
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while (current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    # Forcing our robot to stop
    vel_msg.angular.y = 0
    velocity_publisher.publish(vel_msg)
    rospy.spin()


if __name__ == '__main__':
    try:
        # Testing our function
        turtle()
    except rospy.ROSInterruptException:
        pass
