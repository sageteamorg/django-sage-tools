from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django_sage_tools",
    version="0.1.0",
    author="Sepehr Akbarzadeh",
    author_email="info@sageteam.org",
    description="Reusable, generic mixins for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sageteamorg/django-sage-tools",
    project_urls={
        "Documentation": "https://django-sage-tools.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/sageteamorg/django-sage-tools",
        "Issues": "https://github.com/sageteamorg/django-sage-tools/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.11",
)
