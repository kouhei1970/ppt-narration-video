
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ppt-narration-video",
    version="0.1.0",
    author="",
    author_email="",
    description="PowerPointスライド画像にナレーションを追加して動画として保存するツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ppt-narration-video",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ppt-narration=ppt_narration:main",
        ],
    },
)
