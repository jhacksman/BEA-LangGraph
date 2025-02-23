from setuptools import setup, find_packages

setup(
    name="bea-langgraph",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langgraph",
        "aiohttp",
        "pydantic"
    ]
)
