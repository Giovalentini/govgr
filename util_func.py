import pandas as pd

def scrape_table_data(soup):
    """Scrape table from a page."""
    # Find the table with a specific role
    table = soup.find("table", attrs={"role": "grid"})

    # Initialize an empty list to store the column names
    column_names = []

    # Find the table header row
    header_row = table.find("tr")

    # Extract the column names from the table header
    for th in header_row.find_all("th"):
        # Process or print the column name
        column_names.append(th.text.strip())

    # Initialize an empty DataFrame
    data = pd.DataFrame(columns=column_names)

    # Iterate over the remaining rows in the table
    for row in table.find_all("tr")[1:]:  # Exclude the header row
        # Extract the cells in each row
        cells = row.find_all("td")

        # Create an empty dictionary to store the cell values
        row_data = {}

        for col_index, cell in enumerate(cells):
            # Process or print the cell content along with its column name
            column_name = column_names[col_index]
            cell_content = cell.text.strip()

            # Add the cell content to the row data dictionary
            row_data[column_name] = cell_content

        # Convert the row data list to a DataFrame with a single row
        row_df = pd.DataFrame([row_data], columns=column_names)

        # Concatenate the row DataFrame with the main DataFrame
        data = pd.concat([data, row_df], ignore_index=True)

        # Select only rows added within 1 week from time of execution

    return data