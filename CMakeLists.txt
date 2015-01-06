cmake_minimum_required(VERSION 2.8.3)
project(simple_benchmark)

find_package(catkin REQUIRED
             COMPONENTS message_generation std_msgs rospy)


add_message_files(
   FILES
   StringStamped.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(DEPENDS message_runtime)

install(
    DIRECTORY scripts
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES
  launch/simple_benchmark.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
