from setuptools import setup, find_packages

version = {}
with open('./quadriga/version.py') as fp:
    exec(fp.read(), version)

setup(
    name='quadriga',
    description='Python Wrapper for QuadrigaCX API v2',
    version=version['VERSION'],
    author='Joohwan Oh',
    author_email='joohwan.oh@outlook.com',
    url='https://github.com/joowani/quadriga',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests'],
    tests_require=['pytest', 'mock'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx'
    ]
)
