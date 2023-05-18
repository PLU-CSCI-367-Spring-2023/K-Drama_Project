import csv

# Function to clean up the content_rating data
def clean_content_rating(content_rating):
    # Extract the first two numbers
    cleaned_content_rating = content_rating[:2]
    return cleaned_content_rating

# Path to the input CSV file
input_file = 'top100_kdrama.csv'

# Path to the output CSV file
output_file = 'newTop100_kdrama.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as output:
        # Create a CSV writer
        csv_writer = csv.writer(output)

        # Process each row in the input CSV file
        for row in csv_reader:
            # Clean up the content_rating data
            cleaned_content_rating = clean_content_rating(row[7])

            # Modify the row to replace content_rating with the cleaned value
            row[7] = cleaned_content_rating

            # Write the modified row to the output CSV file
            csv_writer.writerow(row)
