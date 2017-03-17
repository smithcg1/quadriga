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
    tests_require=['pytest', 'mock']
)
