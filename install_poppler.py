import os
import zipfile
import requests

# Get latest release info
print("Checking available poppler releases...")
api_url = 'https://api.github.com/repos/oschwartz10612/poppler-windows/releases/latest'

try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    release_data = response.json()
    
    # Find the Release zip asset (handle any version naming)
    asset_url = None
    for asset in release_data.get('assets', []):
        if 'Release' in asset['name'] and asset['name'].endswith('.zip'):
            asset_url = asset['browser_download_url']
            break
    
    print(f"Found release: {release_data['tag_name']}")
    print(f"Download URL: {asset_url}")
    
    output_zip = os.path.expanduser('~\\AppData\\Local\\Temp\\poppler.zip')
    extract_path = os.path.expanduser('~\\AppData\\Local\\poppler')
    
    os.makedirs(os.path.dirname(output_zip), exist_ok=True)
    os.makedirs(extract_path, exist_ok=True)
    
    print("Downloading poppler...")
    response = requests.get(asset_url, timeout=60)
    response.raise_for_status()
    
    with open(output_zip, 'wb') as f:
        f.write(response.content)
    
    print("Extracting...")
    with zipfile.ZipFile(output_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    poppler_bin = os.path.join(extract_path, 'Library', 'bin')
    print("\n✓ Poppler installed successfully!")
    print("Location:", extract_path)
    print("Bin path:", poppler_bin)
    
except Exception as e:
    print(f"ERROR: {e}")
    print("\nManual installation: Download from https://github.com/oschwartz10612/poppler-windows/releases")
    print("and extract to:", os.path.expanduser('~\\AppData\\Local\\poppler'))
