from setuptools import setup, find_packages
from kbsbot.telegramchannel import __version__

setup(name='cb-telegram-channel',
      description="This is the telegram channel for KBS bot",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=["python-telegram-bot", "requests"],
      author="André Herrera",
      author_email="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices"],
      entry_points={
          'console_scripts': [
              'telegram-channel = kbsbot.telegramchannel.launch:main',
          ],
      }
      )
