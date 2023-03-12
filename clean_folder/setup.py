from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='1.0.0',
      description='Performs sorting of the folder specified in the parameter',      
      author='Friday',
      author_email='i.ufolog@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']})
