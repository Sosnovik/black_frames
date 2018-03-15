from __future__ import print_function
from setuptools import setup
from pip.req import parse_requirements


def run():
	setup(
		name='bframes',
		version='1.0.5',
		packages=['application', 'application.Frames', 'application.Models'],
		url='',
		license='',
		author='V Sosnovik',
		author_email='',
		description='Utility for detecting black frames',
		install_requires=reqs,
		entry_points={
        'console_scripts': ['bframes=application.main:main']
        }
	)

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

MESSAGE = """Tkinter is not installed. Please install it using

\tsudo apt-get install python-tk

or

\tsudo apt-get update
\tsudo apt-get install python3-tk

Then try again
"""

try:
	import tkinter
	imported = 1
except ImportError, e:
	try:
		import Tkinter
		imported = 1
	except:
		print(MESSAGE)

if imported:
	run()



