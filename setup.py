from setuptools import setup, find_packages


def readme():
  with open('README.md', encoding='utf-8') as f:
    README = f.read()
    return README


setup(
  name='thoryvos',
  packages=find_packages(include=['thoryvos']),
  version='1.0.2',
  license='MIT',
  description='The All-In One Cryptographic Toolkit',
  long_description=readme(),
  long_description_content_type='text/markdown',
  author='Rakshan Sharma',
  author_email='rakshan793@gmail.com',
  url='https://github.com/freakingrocky/thoryvos',
  download_url='https://github.com/freakingrocky/thoryvos/build/dist/thoryvos-1.0.2.tar.gz',
  include_package_data=True,
  keywords=['Cryptography', 'Crypto', 'Audio Cryptography',
              'Stagongraphy', 'Steganographer', 'Audio Steganography',
              'Cryptographic Toolkit', 'File Sharing', 'Anonymous File Sharing'],
  install_requires=[
          'PySide2',
          'pycryptodome',
          'argparse',
          'termcolor',
          'PyWave',
          'SoundFile',
          'anonfile'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Other Audience',
    'Intended Audience :: Science/Research',
    'Topic :: Communications :: File Sharing',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Conversion',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'],
  entry_points={
      "console_scripts": [
          "thoryvos=thoryvos.__main__:main",
          "thoryvos_cli=thoryvos.__main__:parse_cl"
      ]
  },
)
