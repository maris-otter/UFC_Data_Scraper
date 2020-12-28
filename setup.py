import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UFC_Data_Scraper",
    version="1.0.0",
    author="Nathan Krieger",
    author_email="kriegerdevelopment@gmail.com",
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
    install_requires=[
         'tqdm', 'requests', 'beautifulsoup4'
     ],
    python_requires='>=3.6',
)
