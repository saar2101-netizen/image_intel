from src.extractor import *
from src.timeline import *

def run_real_test():
    # 1. Set the path to your actual images folder
    # Make sure to change this to your real path!
    folder_path = r"C:\Users\saar2\Desktop\study\python\project\image_intel\images\ready"

    print(f"Extracting data from: {folder_path}...")

    # 2. Get the real data using your function from Step 1
    real_images_data = extract_all(folder_path)

    if not real_images_data:
        print("No images found in the folder. Please check the path.")
        return

    print(f"Found {len(real_images_data)} images. Generating timeline HTML...")

    # 3. Create the HTML using the real data
    html_output = create_timeline(real_images_data)

    # 4. Save the result to an HTML file
    output_filename = "index.html"
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(html_output)

    print(f"Success! Open '{output_filename}' in your web browser to see the real timeline.")


if __name__ == "__main__":
    run_real_test()