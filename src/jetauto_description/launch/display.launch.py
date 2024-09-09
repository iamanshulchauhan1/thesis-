from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument ,SetEnvironmentVariable
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    jetauto_descrpition_dir = get_package_share_directory('jetauto_description')
    return LaunchDescription([
        # Declare arguments
        SetEnvironmentVariable(name ='LIDAR_TYPE' , value= 'G4'),
        SetEnvironmentVariable(name= 'MACHINE_TYPE', value= 'JetAutoPro'),
        SetEnvironmentVariable(name= 'DEPTH_CAMERA_TYPE' , value= 'true'),

        # Set robot description parameter using xacro command
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command([
                    'xacro ', 
                    os.path.join(jetauto_descrpition_dir, 'urdf' , 'jetauto.xacro'), 
                ])
            }]
        ),

        # Launch joint_state_publisher_gui node
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),

        # Launch RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            arguments=['-d', os.path.join(jetauto_descrpition_dir, 'rviz', 'urdf.rviz')],
            output='screen'
        ),
    ])

