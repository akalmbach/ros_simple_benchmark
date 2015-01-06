#! /usr/bin/python

import sys, random, string
import rospy
from std_msgs.msg import Duration
from simple_benchmark.msg import StringStamped

PAYLOAD_TIMESTEP = rospy.Duration(3)

class SimpleBenchmark:
    def __init__(self):
        rospy.init_node("string_pinger")
        
        self.name = rospy.get_param("~name")
        self.othername = rospy.get_param("~othername")
        
        self.dataPub = rospy.Publisher('/'+self.othername+'/data', StringStamped, queue_size=1)
        self.otherDataSub = rospy.Subscriber('/'+self.name+'/data', StringStamped, self.echoMessageCallback)
        self.delayPub = rospy.Publisher('/'+self.name+'/delay', Duration, queue_size=1)
        self.lastTime = rospy.Time.now()
        self.lastPayloadIncreaseTime = rospy.Time()
        self.initialized = False
        self.payloadSize = 1    
        self.echoMessage = StringStamped()
        
        if self.name == 'first':
            r = rospy.Rate(10) # 10hz
            while not rospy.is_shutdown():
                if self.initialized == True:
                    break
                print "Sending init message"
                msg = StringStamped()
                msg.header.stamp = rospy.Time.now();
                msg.data = ""
                self.dataPub.publish(msg)
                r.sleep()
                
        rospy.spin()
        
    def echoMessageCallback(self, msg):
        if not self.initialized:
            self.initialized = True
            self.lastPayloadIncreaseTime = rospy.Time.now()

        if (rospy.Time.now() - self.lastPayloadIncreaseTime > PAYLOAD_TIMESTEP):
            self.lastPayloadIncreaseTime = rospy.Time.now()
            self.payloadSize *= 2
            rospy.loginfo("Increasing payload size to " + str(self.payloadSize))

        self.echoMessage.data = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.payloadSize))
        self.echoMessage.header.stamp = rospy.Time.now()
        delay = msg.header.stamp - self.lastTime
        self.delayPub.publish(Duration(delay))
        self.dataPub.publish(self.echoMessage)
        self.lastTime = msg.header.stamp

        if self.payloadSize > 100:
            rospy.signal_shutdown("finished")
                
if __name__ == "__main__":
    SimpleBenchmark()
