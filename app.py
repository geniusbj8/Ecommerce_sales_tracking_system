from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from fpdf import FPDF

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
sales_data_file = 'sales_data.csv'

# Initialize the sales data file if it doesn't exist
if not os.path.exists(sales_data_file):
    df = pd.DataFrame(columns=["Product Name", "Sales Amount", "Sale Date", "Customer"])
    df.to_csv(sales_data_file, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()
    
    # Validate input data to ensure no field is empty or missing
    required_fields = ["Product Name", "Sales Amount", "Sale Date", "Customer"]
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            return jsonify({"status": f"Error: '{field}' cannot be empty."}), 400

    # Read existing sales data
    sales_data = pd.read_csv(sales_data_file)

    # Create a DataFrame from the new sale data
    new_sale_df = pd.DataFrame([data])

    # Concatenate the new sale DataFrame with the existing sales data
    sales_data = pd.concat([sales_data, new_sale_df], ignore_index=True)
    sales_data.to_csv(sales_data_file, index=False)

    return jsonify({"status": "Sale added successfully!"})

@app.route('/get_sales', methods=['GET'])
def get_sales():
    sales_data = pd.read_csv(sales_data_file)
    return sales_data.to_json(orient='records')

@app.route('/get_sales_summary', methods=['GET'])
def sales_summary():
    # Check if sales data file exists and is not empty
    if os.path.exists(sales_data_file) and os.path.getsize(sales_data_file) > 0:
        sales_data = pd.read_csv(sales_data_file)
    else:
        return jsonify({"status": "No sales data available."}), 404

    # Convert Sales Amount to numeric, handling errors and NaN values
    sales_data['Sales Amount'] = pd.to_numeric(sales_data['Sales Amount'], errors='coerce').fillna(0)

    # Check if there is any valid data after conversion
    if sales_data.empty:
        return jsonify({"status": "Sales data is empty after processing."}), 404

    # Group by 'Product Name' and calculate total sales amount
    total_sales_per_product = sales_data.groupby('Product Name')['Sales Amount'].sum().reset_index()

    # Sort by total sales amount in descending order to find top-selling items
    top_selling_items = total_sales_per_product.sort_values(by='Sales Amount', ascending=False)

    # Get the top 5 selling items
    top_5_items = top_selling_items.head(5)

    # Prepare response summary
    summary = {
        "total_sales_per_product": total_sales_per_product.to_dict(orient='records'),
        "top_selling_items": top_5_items.to_dict(orient='records')
    }

    return jsonify(summary)


@app.route('/plot', methods=['GET'])
def plot():
    sales_data = pd.read_csv(sales_data_file)

    # Convert 'Sale Date' to datetime
    sales_data['Sale Date'] = pd.to_datetime(sales_data['Sale Date'])

    # Plot overall sales trend
    sales_per_day = sales_data.groupby(sales_data['Sale Date'].dt.date)['Sales Amount'].sum()
    plt.figure(figsize=(10, 5))
    plt.plot(sales_per_day.index, sales_per_day.values, marker='o', label='Total Sales')
    
    # Plot individual product sales
    for product_name, product_data in sales_data.groupby('Product Name'):
        daily_sales = product_data.groupby(product_data['Sale Date'].dt.date)['Sales Amount'].sum()
        plt.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='--', label=product_name)
    
    plt.title('Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as an image
    plot_file = 'static/sales_trend.png'
    plt.savefig(plot_file)
    plt.close()

    return jsonify({"plot_url": plot_file})

@app.route('/download_sales_csv', methods=['GET'])
def download_sales_csv():
    return send_file(sales_data_file, as_attachment=True)

@app.route('/download_sales_data_pdf', methods=['GET'])
def download_sales_data_pdf():
    pdf_file = 'static/sales_data.pdf'
    sales_data = pd.read_csv(sales_data_file)

    # Convert 'Sale Date' to datetime
    sales_data['Sale Date'] = pd.to_datetime(sales_data['Sale Date'], errors='coerce')

    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, 'Sales Data Report', ln=True, align='C')
    pdf.ln(10)  # Add a line break

    # Set font for table header
    pdf.set_fill_color(200, 220, 255)  # Light blue background for header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, 'Product Name', 1, 0, 'C', 1)
    pdf.cell(50, 10, 'Sales Amount', 1, 0, 'C', 1)
    pdf.cell(50, 10, 'Sale Date', 1, 0, 'C', 1)
    pdf.cell(50, 10, 'Customer', 1, 1, 'C', 1)  # Use 1 to fill the background

    # Populate the table with sales data
    pdf.set_font("Arial", '', 12)
    for index, row in sales_data.iterrows():
        pdf.cell(50, 10, str(row["Product Name"]), 1)
        pdf.cell(50, 10, str(row["Sales Amount"]), 1)
        pdf.cell(50, 10, row["Sale Date"].strftime('%Y-%m-%d') if pd.notnull(row["Sale Date"]) else 'Invalid Date', 1)
        pdf.cell(50, 10, str(row["Customer"]), 1)
        pdf.ln()

    # Add a summary section at the end
    pdf.ln(10)  # Add a line break
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Summary', ln=True)
    pdf.set_font("Arial", '', 12)
    
    total_sales = sales_data['Sales Amount'].sum()
    total_entries = len(sales_data)
    pdf.cell(0, 10, f'Total Sales Amount: {total_sales}', ln=True)
    pdf.cell(0, 10, f'Total Number of Entries: {total_entries}', ln=True)

    # Include Total Sales per Product
    pdf.ln(10)  # Add a line break
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Total Sales Per Product', ln=True)
    pdf.set_font("Arial", '', 12)

    total_sales_per_product = sales_data.groupby('Product Name')['Sales Amount'].sum().reset_index()
    for index, row in total_sales_per_product.iterrows():
        pdf.cell(0, 10, f"{row['Product Name']}: {row['Sales Amount']}", ln=True)

    # Include Top Selling Items
    pdf.ln(10)  # Add a line break
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Top Selling Items', ln=True)
    pdf.set_font("Arial", '', 12)

    top_selling_items = total_sales_per_product.sort_values(by='Sales Amount', ascending=False).head(5)
    for index, row in top_selling_items.iterrows():
        pdf.cell(0, 10, f"{row['Product Name']}: {row['Sales Amount']}", ln=True)

    # Save the PDF
    pdf.output(pdf_file)

    return send_file(pdf_file, as_attachment=True)

@app.route('/download_sales_plot_pdf', methods=['GET'])
def download_sales_plot_pdf():
    pdf_file = 'static/sales_plot.pdf'
    sales_data = pd.read_csv(sales_data_file)

    # Convert 'Sale Date' to datetime
    sales_data['Sale Date'] = pd.to_datetime(sales_data['Sale Date'], errors='coerce')

    # Check for invalid dates
    if sales_data['Sale Date'].isnull().any():
        return "There are invalid date entries in the data.", 400

    # Group by the date and sum sales
    sales_per_day = sales_data.groupby(sales_data['Sale Date'].dt.date)['Sales Amount'].sum()
    
    plt.figure(figsize=(10, 5))
    plt.plot(sales_per_day.index, sales_per_day.values, marker='o', label='Total Sales')
    
    # Plot individual product sales
    for product_name, product_data in sales_data.groupby('Product Name'):
        daily_sales = product_data.groupby(product_data['Sale Date'].dt.date)['Sales Amount'].sum()
        plt.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='--', label=product_name)
    
    plt.title('Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PDF
    plt.savefig(pdf_file, format='pdf')
    plt.close()

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
