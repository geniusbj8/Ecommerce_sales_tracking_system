$(document).ready(function() {
  $('#submit-sale').click(function() {
      const saleData = {
          "Product Name": $('#product-name').val(),
          "Sales Amount": $('#sales-amount').val(),
          "Sale Date": $('#sale-date').val(),
          "Customer": $('#customer').val()
      };

      $.ajax({
          url: '/add_sale',
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(saleData),
          success: function(response) {
              alert(response.status);
              clearInputs();
          },
          error: function(err) {
              console.error('Error adding sale:', err);
          }
      });
  });

  $('#fetch-sales').click(function() {
      $.ajax({
          url: '/get_sales',
          type: 'GET',
          success: function(data) {
              $('#sales-data').empty();
              
              // Create a table structure
              let table = `<table>
                              <thead>
                                  <tr>
                                      <th>Product Name</th>
                                      <th>Sales Amount</th>
                                      <th>Sale Date</th>
                                      <th>Customer</th>
                                  </tr>
                              </thead>
                              <tbody>`;
              
              // Loop through the sales data and append rows to the table
              const sales = JSON.parse(data);
              sales.forEach(sale => {
                  table += `<tr>
                              <td>${sale["Product Name"]}</td>
                              <td>${sale["Sales Amount"]}</td>
                              <td>${sale["Sale Date"]}</td>
                              <td>${sale["Customer"]}</td>
                            </tr>`;
              });

              table += '</tbody></table>';

              // Append the table to the #sales-data div
              $('#sales-data').append(table);
          },
          error: function(err) {
              console.error('Error fetching sales data:', err);
          }
      });
  });

  $('#fetch-summary').click(function() {
    $.ajax({
        url: '/get_sales_summary',  // Endpoint to fetch summary data
        type: 'GET',
        success: function(data) {
            $('#total-sales').empty();
            $('#top-selling').empty();

            // Total Sales Table
            let totalSalesTable = `<h3>Total Sales per Product</h3>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Product Name</th>
                                                <th>Total Sales Amount</th>
                                            </tr>
                                        </thead>
                                        <tbody>`;
            
            // Update to use data.total_sales_per_product
            const totalSales = data.total_sales_per_product;
            totalSales.forEach(item => {
                totalSalesTable += `<tr>
                                        <td>${item["Product Name"]}</td>
                                        <td>${item["Sales Amount"]}</td>
                                    </tr>`;
            });
            totalSalesTable += '</tbody></table>';
            $('#total-sales').append(totalSalesTable);

            // Top Selling Items Table
            let topSellingTable = `<h3>Top Selling Items</h3>
                                   <table>
                                       <thead>
                                           <tr>
                                               <th>Product Name</th>
                                               <th>Sales Amount</th>
                                           </tr>
                                       </thead>
                                       <tbody>`;
            
            // Update to use data.top_selling_items
            const topSelling = data.top_selling_items;
            topSelling.forEach(item => {
                topSellingTable += `<tr>
                                        <td>${item["Product Name"]}</td>
                                        <td>${item["Sales Amount"]}</td>
                                    </tr>`;
            });
            topSellingTable += '</tbody></table>';
            $('#top-selling').append(topSellingTable);
        },
        error: function(err) {
            console.error('Error fetching sales summary:', err);
        }
    });
});


  $('#show-plot').click(function() {
      $.ajax({
          url: '/plot',
          type: 'GET',
          success: function(data) {
              $('#sales-plot').attr('src', data.plot_url).show();
          },
          error: function(err) {
              console.error('Error generating plot:', err);
          }
      });
  });

  // Download Sales Data as CSV
  $('#download-sales-csv').click(function() {
      window.location.href = '/download_sales_csv';
  });

  // Download Sales Data as PDF
  $('#download-sales-data-pdf').click(function() {
      window.location.href = '/download_sales_data_pdf';
  });

  // Download Sales Plot as PDF
  $('#download-sales-plot-pdf').click(function() {
      window.location.href = '/download_sales_plot_pdf';
  });

  function clearInputs() {
      $('#product-name').val('');
      $('#sales-amount').val('');
      $('#sale-date').val('');
      $('#customer').val('');
  }
});
