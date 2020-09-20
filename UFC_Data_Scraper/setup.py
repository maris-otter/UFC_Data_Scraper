import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kriegernathan1", 
    version="0.0.1",
    author="Nathan Krieger",
    author_email="",
    description="Packages uses BeautifulSoup API to scrape historical data from ufcstat.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kriegernathan1/UFC_Data_Scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
