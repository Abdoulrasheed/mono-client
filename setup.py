import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setuptools.setup(
    version='0.1',
    name='mono_client',
    packages=['mono_client'],
    author='Abdulrasheed Ibrahim',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Access high-quality financial data and perform direct bank payments with mono.co'
)