import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

def scrape_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='a-section a-spacing-medium')
        product_info = []
        for product in products:
            name = product.find('span', class_='a-text-normal').get_text(strip=True)
            price = product.find('span', class_='a-offscreen').get_text(strip=True)
            rating = product.find('span', class_='a-icon-alt').get_text(strip=True).split()[0]
            product_info.append([name, price, rating])
        return product_info
    else:
        messagebox.showerror("Error", "Failed to fetch data from the website.")
        return []

def save_to_csv(product_info, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Price', 'Rating'])
        writer.writerows(product_info)
    messagebox.showinfo("Success", f"Product information saved to '{filename}' successfully.")

def scrape_and_save():
    url = url_entry.get()
    filename = filename_entry.get()
    if not url or not filename:
        messagebox.showerror("Error", "Please enter URL and filename.")
        return
    product_info = scrape_product_info(url)
    if product_info:
        save_to_csv(product_info, filename)
    else:
        messagebox.showerror("Error", "No product information scraped.")

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        filename_entry.delete(0, tk.END)
        filename_entry.insert(0, filename)

root = tk.Tk()
root.title("E-commerce Product Scraper")

url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
filename_entry = tk.Entry(root, width=40)
filename_entry.grid(row=1, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=5, pady=5)

scrape_button = tk.Button(root, text="Scrape and Save", command=scrape_and_save)
scrape_button.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
