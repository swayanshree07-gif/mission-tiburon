from setuptools import setup

package_name = 'perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # notice this matches the folder inside the package
    install_requires=['setuptools', 'opencv-python', 'numpy'],
    zip_safe=True,
    maintainer='Swayanshree',
    maintainer_email='swayanshree07@gmail.com',
    description='Edge detection + color tracking',
    license='MIT',
    entry_points={
        'console_scripts': [
            'p_edge_color = perception.p_edge_color:main',
        ],
    },
)
