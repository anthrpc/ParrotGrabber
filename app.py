from flask import Flask, render_template, request
from selenium import webdriver
import os
from huggingface_hub import hf_hub_download

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    repo_id = request.form['repo_id']
    resource_type = request.form['resource_type']
    folder = request.form['folder']
    extensions = request.form['extensions'].split(',')

    if resource_type == 'model':
        if folder:
            folder = '/'.join(folder.split('/')[1:])
            base_link = f"https://huggingface.co/{repo_id}/tree/main/{folder}"
        else:
            base_link = f"https://huggingface.co/{repo_id}/tree/main"  # Set to root directory
    elif resource_type == 'dataset':
        if folder:
            base_link = f"https://huggingface.co/datasets/{repo_id}/tree/main/{folder}"
        else:
            base_link = f"https://huggingface.co/datasets/{repo_id}/tree/main"  # Set to root directory
    else:
        return "Invalid resource type"

    # Rest of the code remains the same

    driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed and configured
    try:
        driver.get(base_link)
    except:
        return "Failed to access the model/dataset. Please check the accessibility or connection."

    driver.get(base_link)
    # Exclude elements with the specified class from being copied
    exclude_script = "var elements = document.querySelectorAll('.col-span-4.hidden.items-center.truncate.font-mono.text-sm.text-gray-400'); for (var element of elements) { element.remove(); }"
    driver.execute_script(exclude_script)

    driver.execute_script("document.body.focus(); document.execCommand('selectAll');")
    driver.execute_script("document.execCommand('copy');")
    page_content = driver.execute_script("return document.body.innerText;")


    # Process page content to extract relevant file names
    file_names = [name for name in page_content.split('\n') if any(ext in name for ext in extensions)]

    driver.close()

    if not file_names:
        return "No files found matching the specified extensions in the selected folder/model."


    # Iterate through the list of file names and filter out undesired entries
    filtered_file_names = [name.strip() for name in file_names if name.strip()]

    # Write the filtered file names to the text file
    with open("file_names.txt", "w") as file:
        file.write('\n'.join(filtered_file_names))


    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(current_dir, "downloaded_files")
    os.makedirs(download_folder, exist_ok=True)

    cache = os.path.join(current_dir, "cache")
    os.makedirs(cache, exist_ok=True)

    for file_name in file_names:
        # If the folder is specified, concatenate the folder name and file name
        if folder:
            full_file_path = f"{folder}/{file_name}"
            subfolder_name = os.path.dirname(full_file_path)
            subfolder_path = os.path.join(download_folder, subfolder_name)
            os.makedirs(subfolder_path, exist_ok=True)

            download_path = os.path.join(subfolder_path, file_name)
        else:
            full_file_path = file_name
            download_path = os.path.join(download_folder, file_name)

        hf_hub_download(repo_id=repo_id, filename=full_file_path, repo_type=resource_type, local_dir=download_folder, cache_dir=cache)

    return "Files downloaded successfully!"

if __name__ == '__main__':
    app.run()
