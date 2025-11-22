from setuptools import setup, find_packages
import re

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

with open("ghost_frappe/__init__.py") as f:
	version = re.search(r'^__version__\s*=\s*"(.*)"', f.read(), re.M).group(1)

setup(
	name="ghost_frappe",
	version=version,
	description="A professional, headless-ready blogging platform on Frappe.",
	author="Ghost Architect",
	author_email="admin@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
