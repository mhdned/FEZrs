import hashlib
import os
import requests
import yaml

# Function to read version from the VERSION file
def read_version_from_file(version_file="VERSION"):
    with open(version_file, "r") as file:
        return file.read().strip()

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

# Function to update the meta.yaml file with new SHA256 and version
def update_meta_yaml(meta_yaml_path, new_sha256, version):
    with open(meta_yaml_path, 'r') as file:
        meta = yaml.safe_load(file)
    
    # Update the version and SHA256 field in the meta.yaml file
    meta['package']['version'] = version
    meta['source']['sha256'] = new_sha256
    
    # Write the updated YAML back to file
    with open(meta_yaml_path, 'w') as file:
        yaml.dump(meta, file, default_flow_style=False)
    print(f"Updated meta.yaml with version {version} and new SHA256: {new_sha256}")

# Main function
def main():
    # Read the version from the VERSION file
    version = read_version_from_file()  # By default it looks for a file named 'VERSION'
    
    # Define the package URL and destination for downloading
    url = f"https://pypi.io/packages/source/f/fezrs/fezrs-{version}.tar.gz"
    dest_path = f"fezrs-{version}.tar.gz"
    
    # Download the source file
    download_source(url, dest_path)
    
    # Calculate the SHA256 checksum
    new_sha256 = calculate_sha256(dest_path)
    
    # Path to your meta.yaml file
    meta_yaml_path = "recipe/meta.yaml"
    
    # Update the meta.yaml file with the new version and SHA256
    update_meta_yaml(meta_yaml_path, new_sha256, version)
    
    # Set the version as an environment variable for conda build
    os.environ["VERSION"] = version

    # Trigger the Conda build
    os.system("conda build recipe/")

if __name__ == "__main__":
    main()
