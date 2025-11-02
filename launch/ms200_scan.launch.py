#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

'''
parameters=[
        {'device_model': 'MS200'},
        {'frame_id': 'laser_frame'},
        {'scan_topic': 'sensors/lidar/scan_raw'},
        {'port_name': '/dev/ttyUSB0'},
        {'baudrate': 230400},
        {'angle_min': 0.0},
        {'angle_max': 360.0},
        {'range_min': 0.05},
        {'range_max': 20.0},
        {'clockwise': False},
        {'motor_speed': 10}
      ]
'''

def generate_launch_description():
  frame_id = LaunchConfiguration('frame_id')
  topic_name = LaunchConfiguration('topic_name')
  port_name = LaunchConfiguration('port_name')

  declare_frame_id = DeclareLaunchArgument(
      'frame_id',
      default_value='laser_frame',
      description='TF frame for the lidar'
  )

  declare_topic_name = DeclareLaunchArgument(
      'topic_name',
      default_value='sensors/lidar/scan_raw',
      description='Topic name for raw lidar scans'
  )

  declare_port_name = DeclareLaunchArgument(
      'port_name',
      default_value='/dev/ttyUSB0',
      description='Serial port used by the lidar'
  )

  # LiDAR publisher node
  ordlidar_node = Node(
      package='oradar_lidar',
      executable='oradar_scan',
      name='MS200',
      output='screen',
      parameters=[{
        'device_model': 'MS200',
        'frame_id': frame_id,
        'scan_topic': topic_name,
        'port_name': port_name,
        'baudrate': 230400,
        'angle_min': 0.0,
        'angle_max': 360.0,
        'range_min': 0.05,
        'range_max': 20.0,
        'clockwise': False,
        'motor_speed': 10
      }]
  )

  # base_link to laser_frame tf node
  base_link_to_laser_tf_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='base_link_to_base_laser',
    arguments=['0','0','0.18','0','0','0','base_link', frame_id]
  )


  # Define LaunchDescription variable
  ord = LaunchDescription([
      declare_frame_id,
      declare_topic_name,
      declare_port_name,
      ordlidar_node,
      base_link_to_laser_tf_node
  ])

  return ord
