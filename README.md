# E-Commerce Draft

First create a virtual environment to accomodate the application:

    python -m venv venv

Then activate the environment each time you want to use the application.
Instructions for Windows:

    venv/Scripts/Activate.ps1

After activation you can install project requirements:

    pip install -r ./requirements.txt

Run it with:

    flask --app ecommerce.web --debug run


Before you commit, run quality check tools:

    black .
    isort .
    pylint ecommerce
