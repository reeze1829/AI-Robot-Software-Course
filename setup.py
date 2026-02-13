from setuptools import setup
import os
from glob import glob

package_name = 'ros2_personal_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # UI 파일을 설치 경로로 복사하는 설정 (매우 중요!)
        (os.path.join('share', package_name, 'ui'), glob('ui/*.ui')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kim',
    maintainer_email='user@todo.todo',
    description='Gazebo Robot GUI Control Project',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 실행 명령어 = 패키지명.파일명:함수명
            'main_node = ros2_personal_project.main_node:main',
        ],
    },
)
