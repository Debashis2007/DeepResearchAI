"""
Script to deploy Deep Research AI to Hugging Face Spaces.
"""

from huggingface_hub import HfApi, create_repo, upload_folder
import os

# Configuration
SPACE_NAME = "deep-research-ai"
USERNAME = "debashis2007"
REPO_ID = f"{USERNAME}/{SPACE_NAME}"

def deploy():
    """Deploy to Hugging Face Spaces."""
    api = HfApi()
    
    print(f"🚀 Deploying to {REPO_ID}...")
    
    # Create the Space (or get existing)
    try:
        create_repo(
            repo_id=REPO_ID,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True
        )
        print(f"✅ Space created/verified: https://huggingface.co/spaces/{REPO_ID}")
    except Exception as e:
        print(f"⚠️ Repo creation: {e}")
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Upload the folder
    print("📤 Uploading files...")
    api.upload_folder(
        folder_path=current_dir,
        repo_id=REPO_ID,
        repo_type="space",
        ignore_patterns=[
            ".git/*",
            "__pycache__/*",
            "*.pyc",
            ".env",
            ".DS_Store",
            "tests/*",
            "requirement/*",
            "prompt/*",
            "deploy.py",
            "README.md",  # We'll use README_HF.md as README
            "requirements.txt",  # We'll use requirements_hf.txt
        ]
    )
    
    # Upload README_HF.md as README.md
    print("📝 Uploading README...")
    api.upload_file(
        path_or_fileobj=os.path.join(current_dir, "README_HF.md"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="space"
    )
    
    # Upload requirements_hf.txt as requirements.txt
    print("📦 Uploading requirements...")
    api.upload_file(
        path_or_fileobj=os.path.join(current_dir, "requirements_hf.txt"),
        path_in_repo="requirements.txt",
        repo_id=REPO_ID,
        repo_type="space"
    )
    
    print(f"""
✅ Deployment complete!

🔗 Your Space: https://huggingface.co/spaces/{REPO_ID}

Note: It may take a few minutes for the Space to build and start.
""")

if __name__ == "__main__":
    deploy()
