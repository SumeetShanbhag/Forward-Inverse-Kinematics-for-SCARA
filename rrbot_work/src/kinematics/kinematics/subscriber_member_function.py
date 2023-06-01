import math
import rclpy                                             #rcply and math required libraries
from rclpy.node import Node
from sensor_msgs.msg import JointState     
from geometry_msgs.msg import Pose        

# Pub Code: ros2 topic pub /topic_name std_msgs/msg/Float32MultiArray 'data: [0,0,0]'

class minimal_subscriber(Node):                               #Create Subscriber Class, inheriting from Node Class  

    def __init__(self):
        super().__init__('minimal_subscriber')        #Calling the constructor of Node class and giving it name of 'subscriber'
        self.sub = self.create_subscription(JointState, 'joint_states', self.chatter_callback, 10)     #Declaring that the node subscribes to message of type Float32MultiArray and topic name is 'topic_name'  and to receive it from chatter_callback function, with queue size 10.

    def chatter_callback(self, msg):
    
        q1=msg.position[0]           #joint one theta value
        q2=msg.position[1]           #joint two theta value
        d =msg.position[2]           #joint three translation value
        
        #applying cosines and sines for easy computation
        cq1 = math.cos(q1)
        sq1 = math.sin(q1)
        cq2 = math.cos(q2)
        sq2 = math.sin(q2)
        
        # Forward kinematics equations (derived from MATLAB)
        x11 = cq1*cq2 - sq1*sq2
        x12 = -(sq1*cq2 + cq1*sq2)
        x13 = 0
        x21 = (sq1*cq2 + cq1*sq2)
        x22 = cq1*cq2 - sq1*sq2
        x23 = 0
        x31 = 0
        x32 = 0
        x33 = 1
        x14 = 0.9*cq1 + cq1*cq2 - sq1*sq2
        x24 = 0.9*sq1 + sq1*cq2 + cq1*sq2
        x34 = d + 1.2
        x41 = 0
        x42 = 0 
        x43 = 0 
        x44 = 1
        
        # Extracting x, y and z from the matrix as translation values for fkin calculations 
        x = x14
        y = x24
        z = x34
    	
        #publishing these values to ikin for calculations
        self.publisher_ = self.create_publisher(Pose, 'fkin_topic', 10)
        msg = Pose()
        msg.position.x = x
        msg.position.y = y
        msg.position.z = z
        self.publisher_.publish(msg)
    	
        #forming the matrix to be displayed
        str1 = "\t|\t"+str(x11) + "\t" + str(x12) + "\t" + str(x13) + "\t" + str(x14)+"\t|\n"
        str2 = "\t|\t"+str(x21) + "\t" + str(x22) + "\t" + str(x23) + "\t" + str(x24)+"\t|\n"
        str3 = "\t|\t"+str(x31) + "\t" + str(x32) + "\t" + str(x33) + "\t" + str(x34)+"\t|\n"
        str4 = "\t|\t"+str(x41) + "\t" + str(x42) + "\t" + str(x43) + "\t" + str(x44)+"\t|\n"
        output_str = str1 + str2 + str3 + str4
        self.get_logger().info(f'\n\n\nFor q = ' + '(' + str(q1) + ", " + str(q2) + ", " + str(d) + "):\n"+'T3_0:\n' + output_str)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(minimal_subscriber())
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
