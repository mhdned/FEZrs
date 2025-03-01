import hashlib
import os
import requests
import yaml

# Function to calculate SHA256 checksum of a file
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Function to download the source file
def download_source(url, dest_path):
    response = requests.get(url, stream=True)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {url} to {dest_path}")

# Function to update the meta.yaml file with new SHA256
def update_meta_yaml(meta_yaml_path, new_sha256):
    with open(meta_yaml_path, 'r') as file:
        meta = yaml.safe_load(file)
    
    # Update the SHA256 field in the source section
    meta['source']['sha256'] = new_sha256
    
    # Write the updated YAML back to file
    with open(meta_yaml_path, 'w') as file:
        yaml.dump(meta, file, default_flow_style=False)
    print(f"Updated meta.yaml with new SHA256: {new_sha256}")

# Main function
def main():
    # Define the package URL and destination for downloading
    version = "0.4.11"  # Update as per your version
    url = f"https://pypi.io/packages/source/f/fezrs/fezrs-{version}.tar.gz"
    dest_path = f"fezrs-{version}.tar.gz"
    
    # Download the source file
    download_source(url, dest_path)
    
    # Calculate the SHA256 checksum
    new_sha256 = calculate_sha256(dest_path)
    
    # Path to your meta.yaml file
    meta_yaml_path = "recipe/meta.yaml"
    
    # Update the meta.yaml file with the new SHA256
    update_meta_yaml(meta_yaml_path, new_sha256)
    
    # Optionally, trigger the build
    os.system("conda build recipe/")
    
if __name__ == "__main__":
    main()
