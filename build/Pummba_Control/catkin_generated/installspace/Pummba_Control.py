#!/home/nubot/Documents/Study/PythonEnv/ros-py3-tf1/bin/python3.6
# license removed for brevity
import rospy
from geometry_msgs.msg import Pose
from nubot_pummba_msg.msg import PummbaCmd


def node_init():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    global cmd_pub, rate, pummba_cmd, pummba_state
    pummba_cmd = PummbaCmd()
    pummba_state = Pose()

    rospy.init_node('Nubot_Control', anonymous=True)
    rospy.Subscriber("Nubot_Pummba/nubotstate/robotstate", Pose, robotstate_CB)
    cmd_pub = rospy.Publisher('Nubot_Pummba/nubotcontrol/pummbacmd', PummbaCmd, queue_size=10)
    rate = rospy.Rate(10)  # 10hz
    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()


def robotstate_CB(_msg):
    # global pummba_state
    pummba_state = _msg
    rospy.loginfo(rospy.get_caller_id() + " %f", pummba_state.position.x)


if __name__ == '__main__':
    try:
        node_init()
        while not rospy.is_shutdown():
            rospy.loginfo("pummba_state %f %f", pummba_state.position.x, pummba_state.orientation.x)
            pummba_cmd.vel_linear = 0.5
            pummba_cmd.vel_angular = -0.5
            pummba_cmd.front_left = 1
            pummba_cmd.front_right = 1
            pummba_cmd.rear_left = 1
            pummba_cmd.rear_right = 1
            rospy.loginfo("pummba_cmd_track %f %f", pummba_cmd.vel_linear, pummba_cmd.vel_angular)
            rospy.loginfo("pummba_cmd_flip %f %f %f %f", pummba_cmd.front_left, pummba_cmd.front_right, pummba_cmd.rear_left,
                        pummba_cmd.rear_right)
            cmd_pub.publish(pummba_cmd)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
