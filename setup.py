import pathlib
import setuptools

setuptools.setup(
    name="resmushit",
    version="1.0.0",
    description="A wrapper for resmush.it API",
    long_description=pathlib.Path("README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    url="https://resmush.it/",
    author="Hemant Sah",
    author_email="hemantsah18@gmail.com",
    maintainer="Hemant Sah",
    license="MIT",
    project_urls={
        "Homepage":"https://resmush.it/",
        "Documentation":"https://github.com/hemansah/resmushit/blob/master/README.md",
        "Repository":"https://github.com/hemansah/resmushit/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6,<=3.12",
    install_requires=['urllib3', 'colorama'],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
