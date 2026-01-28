# Connect VSCode to Google Colab

## Method 1: Using Google Drive Sync (Simplest)

### Setup:
1. **Upload your project to Google Drive:**
   - Create a folder in Google Drive: `MyDrive/BertModel`
   - Upload your local files to this folder

2. **In Google Colab:**
   - Create a new notebook
   - Run this code:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   
   # Navigate to your project
   %cd /content/drive/MyDrive/BertModel
   
   # Run your code
   !python demo.ipy
   ```

3. **Workflow:**
   - Edit files locally in VSCode
   - Save to Google Drive (use Google Drive desktop app for auto-sync)
   - Run in Colab
   - Changes sync back automatically

---

## Method 2: Using colabcode (VSCode in Browser)

### Setup:
1. **Open Google Colab**
2. **Install and run colabcode:**
   ```python
   !pip install colabcode
   from colabcode import ColabCode
   ColabCode(port=10000, password="your_password")
   ```
3. **Click the generated link** to access VSCode in your browser
4. **Write and run code** directly in the cloud

---

## Method 3: Using Jupyter Remote Kernel

### Setup:
1. **In Google Colab, install jupyter:**
   ```python
   !pip install jupyter
   !pip install jupyter_http_over_ws
   !jupyter serverextension enable --py jupyter_http_over_ws
   ```

2. **Start Jupyter server with authentication:**
   ```python
   !jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' \
     --port=8888 --NotebookApp.port_retries=0 --no-browser
   ```

3. **Install Jupyter extension in VSCode**
4. **Connect to the remote kernel** using the token provided

---

## Method 4: Manual Upload/Download (Quick Testing)

### For quick tests:
1. **Upload to Colab:**
   ```python
   from google.colab import files
   uploaded = files.upload()  # Select your local file
   ```

2. **Run the code:**
   ```python
   !python demo.ipy
   ```

3. **Download results:**
   ```python
   files.download('output_file.txt')
   ```

---

## Recommended Workflow

**For BERT Model Development:**

1. **Use Google Drive Sync** for seamless file synchronization
2. **Install Google Drive desktop app** on your PC
3. **Save your VSCode workspace** in the Google Drive folder
4. **In Colab:**
   - Mount Drive
   - Navigate to project folder
   - Install dependencies (transformers, torch, etc.)
   - Run your training scripts

### Example Colab Notebook:
```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Navigate to project
%cd /content/drive/MyDrive/BertModel

# Install dependencies
!pip install transformers torch torchvision

# Run your demo
!python demo.ipy

# Or import and run
import demo
```

---

## Tips:
- ✓ Use `.ipynb` files for better Colab integration
- ✓ Colab provides free GPU/TPU (Runtime → Change runtime type)
- ✓ Sessions timeout after 12 hours of inactivity
- ✓ Save outputs back to Drive before session ends
