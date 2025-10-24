# # from setuptools import setup, find_packages

# # setup(
# #     name="codehouse_cyb",
# #     version="1.2.0",
# #     description="CodeHouse Cybersecurity CLI Trainer",
# #     author="CodeHouse",
# #     packages=find_packages(),
# #     include_package_data=True,
# #     install_requires=[
# #         "requests>=2.0.0",
# #         "rich>=13.0.0",
# #         "colorama>=0.4.0",
# #         "rapidfuzz>=3.0.0"
# #     ],
# #     classifiers=["Programming Language :: Python :: 3"],
# #     python_requires=">=3.8",
# # )
# # setup.py
# from setuptools import setup, find_packages
# from pathlib import Path

# this_directory = Path(__file__).parent
# long_description = ""
# readme = this_directory / "README.md"
# if readme.exists():
#     long_description = readme.read_text(encoding="utf-8")

# setup(
#     name="codehouse_cyb",          # must be unique on PyPI
#     version="1.0.0",
#     author="Applinet Technology",
#     author_email="support@applinet.africa",
#     description="A cybersecurity training client package for Codehouse.",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/applinet-technology/codehouse_cyb",
#     license="MIT",
#     packages=find_packages(exclude=("tests",)),
#     include_package_data=True,
#     install_requires=[
#         "requests",
#         "rich",
#         # rapidfuzz is optional but recommended. If you want to make it optional, handle ImportError in code.
#         "rapidfuzz>=3.0.0",
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.8",
#     entry_points={
#         "console_scripts": [
#             # This creates a command 'cyb-start' that runs cyb.start:main
#             "cyb-start=cyb.start:main",
#         ],
#     },
# )
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="codehouse_cyb",  # unique package name
    version="1.0.0",
    author="Applinet Technology (Godswill Moses Ikpotokin)",
    author_email="developers@applinet.com.ng",
    description="CodeHouse Cybersecurity Training CLI — Learn, Practice, and Log Cybersecurity Quizzes from CodeHouse Cloud.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/applinet-technology/codehouse_cyber_quiz",
    project_urls={
        "Homepage": "https://cli.codehouse.cloud",
        "Applinet Technology": "https://applinet.com.ng",
        "Source": "https://github.com/applinet-technology/codehouse_cyber_quiz",
        "Issues": "https://github.com/applinet-technology/codehouse_cyber_quiz/issues",
    },
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "rapidfuzz>=3.6.0",
        "click>=8.1.7",
        "python-dateutil>=2.9.0",
        "tinydb>=4.8.0",
        "python-dotenv>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "cyb-start=cyb.start:main",  # CLI command to launch the training
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
)
