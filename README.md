# Data scrapping demo

For ease of use, use [Poetry](https://python-poetry.org/)

## Installation and Usage

### Using Poetry

1. Install Poetry
    >Poetry provides a custom installer that will install `poetry` isolated from the rest of your system.

    #### osx / linux / bashonwindows install instructions
    ```bash
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
    ```
    #### windows powershell install instructions
    ```powershell
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content   | python -
    ```

2. Install Dependencies
   ```bash
    poetry install
   ```

3. Run the script 
   ```bash
   poetry run main
   ```

### Using requirements.txt

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script
    ```bash
    python dataextractor_amazon/main.py
    ```
