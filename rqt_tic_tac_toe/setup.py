from setuptools import setup

package_name = 'rqt_tic_tac_toe'
setup(
    name=package_name,
    version='1.0.0',
    package_dir={'': 'src'},
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/resource', ['resource/TicTacToeWidget.ui']),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugin.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ShotaAk',
    maintainer='ShotaAk',
    maintainer_email='macakasit@gmail.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description=(
        'rqt_tic_tac_toe provides a GUI plugin to play Tic-Tac-Toe.'
    ),
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_tic_tac_toe = ' + package_name + '.main:main',
        ],
    },
)