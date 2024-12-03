# SaleTrack: E-commerce Sales Tracking System

SaleTrack is a web-based application built with Flask and JavaScript, designed to track sales data in an organized, visually appealing way. It allows users to add new sales, view summaries, and download data and plots in various formats for easy analysis.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## Features

- **Add Sales**: Enter product name, sales amount, sale date, and customer information.
- **View Sales Data**: Display all sales records in a table format.
- **Sales Summary**: Show total sales per product and the top-selling items.
- **Sales Plot**: Visualize daily sales trends, including individual product sales.
- **Download Options**: Export data as CSV and PDF, and download plots as PDF.

## Setup

1. **Prerequisites**:
   - Python 3.12.2
   - Flask (`pip install Flask`)
   - Pandas (`pip install pandas`)
   - Matplotlib (`pip install matplotlib`)
   - FPDF (`pip install fpdf`)

2. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Set Up Virtual Environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate  # On Windows
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your browser and go to `http://127.0.0.1:5000/`.


## Usage

- **Add a Sale**: Fill in the product name, sales amount, sale date, and customer name, then click "Submit Sale".
- **Fetch Sales Data**: Click "Fetch Sales Data" to view all sales in a table format.
- **Download Data**: 
  - CSV: Click "Download Sales Data (CSV)".
  - PDF: Click "Download Sales Data Report (PDF)" for a detailed report with summaries.
- **Plot Sales**: Click "Show Sales Plot" to view the sales trend graph. You can also download this plot as a PDF.

## API Endpoints

### `POST /add_sale`
- **Description**: Adds a new sale record.
- **Request**: JSON object with keys `Product Name`, `Sales Amount`, `Sale Date`, and `Customer`.
- **Response**: Success or error message.

### `GET /get_sales`
- **Description**: Retrieves all sales data.
- **Response**: JSON array with all sales records.

### `GET /get_sales_summary`
- **Description**: Provides a summary of total sales per product and top-selling items.
- **Response**: JSON object with summaries.

### `GET /plot`
- **Description**: Generates and returns the URL of the sales trend plot.
- **Response**: JSON object with `plot_url` containing the path to the plot image.

### `GET /download_sales_csv`
- **Description**: Downloads sales data in CSV format.

### `GET /download_sales_data_pdf`
- **Description**: Downloads a detailed PDF report of sales data.

### `GET /download_sales_plot_pdf`
- **Description**: Downloads the sales trend plot as a PDF.

## Troubleshooting

1. **Server Error 500**:
   - Check if all dependencies are installed.
   - Ensure there are no invalid entries in the sales data file (`sales_data.csv`).

2. **Plot Not Displaying**:
   - Verify that the sales data file exists and contains data.
   - Check for any invalid dates in the `Sale Date` column in `sales_data.csv`.

3. **CSV/ PDF Download Fails**:
   - Ensure the `static` directory has appropriate read/write permissions.
   - Check if the files `sales_data.csv` and `sales_data.pdf` exist in the project directory.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.

---

Enjoy using SaleTrack! For any questions or issues, please open an issue on the repository.
