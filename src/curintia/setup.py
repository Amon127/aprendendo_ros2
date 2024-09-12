from setuptools import find_packages, setup

package_name = 'curintia'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/batata.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mário Amon',
    maintainer_email='amonmrodrigues@gmail.com',
    description='Pacote para o exercício',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'roger_guedes = curintia.roger_guedes:main',
            'yuri_alberto = curintia.yuri_alberto:main',
        ],
    },
)
