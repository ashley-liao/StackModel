from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import perfevents

# Specify the path to your extension
extension_path = '/home/chenye/StackModel-Extension Version'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f"--load-extension={extension_path}")
chrome_options.add_argument('--enable-precise-memory-info')
url_path = '/home/chenye/StackModel-Extension Version/testing/filtered-urls.csv'
output_path = '/home/chenye/StackModel-Extension Version/testing/metrics.csv'

# Initialize an empty list to hold URLs
urls = []


# Read URLs from the CSV file
with open(url_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        urls.append(row[0])
    
with open(output_path, mode='w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['URL', 'onContentLoad', 'onLoad', 'JSHeapSize', 'cpu-clock', 'cpu-migrations', 'context-switches', 'page-faults', 'task-clock'])       
    for url in urls:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            perf = perfevents.PerfEvents(30)
            
            time.sleep(15)
            
            perf.start()
            driver.get(url)
            navigation_timing = driver.execute_script("return window.performance.timing.toJSON();")
            on_content_load = navigation_timing['domContentLoadedEventEnd'] - navigation_timing['navigationStart']
            on_load = navigation_timing['loadEventEnd'] - navigation_timing['navigationStart']
            memory_usage = driver.execute_script("return window.performance.memory.usedJSHeapSize;")
            try:
                perf_data = perf.stop()
            except Exception as e:
                print(f"Error stopping perf events for URL {url}: {e}")
                continue
            performance_metrics = {key: 'N/A' for key in ['cpu-clock', 'cpu-migrations', 'context-switches', 'page-faults', 'task-clock']}
            for event, value in perf_data.items():
                if event in performance_metrics:
                    performance_metrics[event] = value
            print([url, on_content_load, on_load, memory_usage, performance_metrics['cpu-clock'], performance_metrics['cpu-migrations'],
            performance_metrics['context-switches'], performance_metrics['page-faults'],
            performance_metrics['task-clock']])
            csv_writer.writerow([url, on_content_load, on_load, memory_usage, performance_metrics['cpu-clock'], performance_metrics['cpu-migrations'], performance_metrics['context-switches'], performance_metrics['page-faults'], performance_metrics['task-clock']])
        except Exception as e:
            continue        
        finally:
            driver.quit()