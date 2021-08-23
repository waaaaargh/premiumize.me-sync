from setuptools import setup, find_packages

setup(name="premiumizeme_sync",
      version="0.1.0",
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=[
          'fire>=0.4.0', 'requests>=2.26.0', 'marshmallow>=3.13.0',
          'marshmallow_dataclass>=8.5.3', 'marshmallow_enum>=1.5.1'
      ],
      entry_points={
          'console_scripts':
          ['premiumizeme-sync=premiumizeme_sync.cli.main:main']
      })
