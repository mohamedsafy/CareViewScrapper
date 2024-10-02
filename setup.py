from setuptools import setup

APP = ['main.py']  # Replace with your script name
DATA_FILES = []  # List additional files you want to include
OPTIONS = {
    'argv_emulation': True,
    'packages': ['beautifulsoup4','pandas', 'selenium', 'webdriver_manager'],  # List your required packages here
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
