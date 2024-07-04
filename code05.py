import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import csv


def scrape_data():
    def perform_scraping():
        url = entry_url.get()
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if not url or not csv_file_path:
            messagebox.showerror("Error", "Please provide a valid URL and select a save location.")
            return

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select('.product')

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Product Name", "Price", "Rating"])

                for product in products:
                    product_name = product.select_one('.product-name').get_text(strip=True)
                    price = product.select_one('.product-price').get_text(strip=True)
                    rating = product.select_one('.product-rating').get_text(strip=True)
                    writer.writerow([product_name, price, rating])

            messagebox.showinfo("Success", f"Data has been successfully scraped and saved to {csv_file_path}")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error connecting to the website: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    scrape_window = tk.Tk()
    scrape_window.title("Web Scraping")

    tk.Label(scrape_window, text="Enter URL:").pack()
    entry_url = tk.Entry(scrape_window, width=50)
    entry_url.pack()

    tk.Button(scrape_window, text="Scrape Data", command=perform_scraping).pack()

    scrape_window.mainloop()


if __name__ == "__main__":
    scrape_data()
