<!-- Project Shields -->
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)

# Interactive Menu Engineering Dashboard
A full-stack web application that visualizes restaurant menu item performance using Menu Engineering principles (Star, Puzzle, Plowhorse, Dog). This tool helps restaurant owners and analysts make data-driven decisions to optimize pricing, profitability, and sales strategy.

## Built With
* ![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=plastic&logo=flask&logoColor=white)
* ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=plastic&logo=javascript&logoColor=%23F7DF1E)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=plastic&logo=postgresql&logoColor=white)
* ![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=plastic&logo=chart.js&logoColor=white)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=plastic&logo=docker&logoColor=white)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=plastic&logo=numpy&logoColor=white)
* ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=plastic&logo=pandas&logoColor=white)
* ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=plastic&logo=Matplotlib&logoColor=black)
* ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=plastic&logo=tailwind-css&logoColor=white)
* ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=plastic&logo=html5&logoColor=white)

## Features
* Quadrant Classification of menu items: Star, Plowhorse, Puzzle, Dog

* Interactive Chart built with Chart.js for visualizing item performance

* Displays average price vs. quantity sold with color-coded markers

* Key metrics: total items, sales totals, and quadrant breakdowns

* Dynamic menu performance table with pricing and sales data

* ETL-ready: supports importing raw sales data for preprocessing


## Getting Started: Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/menu-dashboard.git
    cd menu-dashboard
    ```
2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```
4. Set environment variables (optional for development):
    ```sh
    export FLASK_APP=run.py
    export FLASK_ENV=development
    ```
5. Run the Flask app:
    ```sh
    flask run
    ```
6. Visit the dashboard:
    ```sh
    http://localhost:PORT/
    ```
### Docker (Optional):
```sh
docker-compose up --build
```
### Sample Data Format
The ```raw_sales_data.csv``` file should contain:

| item_name | group | avg_price | qty_sold | net_sales |
| :---: | :---: | :---: | :---: | :---: |
###
The ```etl.py``` script will process this data and assign menu quadrants automatically.

#### OR

run:
```sh
flask etl
```
## Usage

### Menu Engineering Quadrants

| Quadrant| Description|
| :---| ---:|
| Star | High Sales, High Price
| Workhorse | High Sales, Low Price
| Puzzle | Low Sales, High Price
| Dog | Low Sales, Low Price

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## Author
Emmanuel Lakis

## License
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=plastic)](./LICENSE)

# Badges