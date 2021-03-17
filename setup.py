from setuptools import setup


def readme_file_contents():
    with open("Readme.rst") as readme_file:
        data = readme_file.read()
    return data


setup(
    name='tcppot',
    version='1.0',
    description='Simple TCP honeypot for Pi',
    long_description=readme_file_contents(),
    author='Shirshu',
    packages=['tcppot'],
    zip_safe=False,
    Install_requires=[]
)
