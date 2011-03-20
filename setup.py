from setuptools import setup

version = '1.0b1'


setup(name='ohconvert',
      version=version,
      description="ohconvert integrates ohcount into Jenkins.",
      long_description=open("README.txt").read() + "\n" + \
                       open("CHANGES.txt").read(),
      classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
      keywords='ohcount jenkins sloccount',
      author='Hanno Schlichting, Laurence Rowe',
      author_email='hanno@hannosch.eu',
      url='http://pypi.python.org/pypi/ohconvert',
      license='BSD',
      package_dir={'': 'src'},
      py_modules=['ohconvert'],
      zip_safe=False,
      install_requires=['setuptools'],
      entry_points="""
      [console_scripts]
      ohconvert=ohconvert:main
      """,
      )
