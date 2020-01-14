import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="i3wins",
    version="0.0.4",
    author="Yoann Lamouroux",
    author_email="ylamouroux@ubuntu.com",
    description="Yet another i3 window switcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ylmrx/i3wins",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['i3ipc', 'dynmen', 'traitlets'],
    entry_points={
        'console_scripts': [
            'i3wins=i3wins.i3wins:main',
            'i3lasts=i3wins.i3lasts:server',
            'i3lastc=i3wins.i3lasts:client'
        ]
    }
)

