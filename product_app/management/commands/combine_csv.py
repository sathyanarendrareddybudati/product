from django.core.management.base import BaseCommand
import csv
import os


class Command(BaseCommand):

    help = 'Merge multiple CSV files into a single CSV file with headers'

    def handle(self, *args, **kwargs):
        input_files = ['/Users/satyanarendrareddybudati/Documents/ApplePay.csv',
                        '/Users/satyanarendrareddybudati/Documents/PhonePe.csv',
                        '/Users/satyanarendrareddybudati/Documents/Website.csv']
        output_file = 'transaction_report.csv'

        headers = ["first_name", "last_name", "email", "phone", "address", "transaction_id", "transaction_at", "created_at"]

        with open(output_file, 'w', newline='') as merged_csv:
            writer = csv.DictWriter(merged_csv, fieldnames=headers)
            writer.writeheader()

            for input_file in input_files:
                with open(input_file, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Filter out keys not present in headers
                        row = {key: row[key] for key in headers if key in row}
                        writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"CSV files merged successfully into {output_file}"))

