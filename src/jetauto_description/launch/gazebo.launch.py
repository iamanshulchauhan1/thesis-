import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, Command

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('odom_frame', default_value='odom', description='Odometry frame'),
        DeclareLaunchArgument('base_frame', default_value='base_footprint', description='Base frame'),
        DeclareLaunchArgument('depth_camera_name', default_value='camera', description='Depth camera name'),
        DeclareLaunchArgument('robot_description', default_value='xacro path/to/your/urdf/jetauto.urdf.xacro odom_frame:=$(arg odom_frame) base_frame:=$(arg base_frame) depth_camera_name:=$(arg depth_camera_name)', description='Command to generate robot description'),

        # Start Gazebo server with empty world
        Node(
            package='gazebo_ros',
            executable='gzserver',
            name='gazebo',
            output='screen',
            arguments=['-s', 'libgazebo_ros_factory.so']
        ),
        Node(
            package='gazebo_ros',
            executable='gzclient',
            name='gazebo_client',
            output='screen',
        ),
        # Spawn the robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_model',
            output='screen',
            arguments=['-entity', 'jetauto', '-file', LaunchConfiguration('robot_description')]
        ),
        # Fake joint calibration
        Node(
            package='rosapi',  # Replace with the actual package providing `rostopic` if available
            executable='rostopic',
            name='fake_joint_calibration',
            output='screen',
            arguments=['pub', '/calibrated', 'std_msgs/Bool', 'true']
        ),
    ])

