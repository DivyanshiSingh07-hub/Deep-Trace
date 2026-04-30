import zipfile
import os
import random

celeb_zip_path = r'E:\Khushi\Downloads\Celeb-DF-v2.zip'
cifake_zip_path = r'E:\Khushi\Downloads\archive.zip'
output_dir = r'D:\Khushi\Documents\DEEP\new_data'

os.makedirs(os.path.join(output_dir, 'real'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'fake'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'cifake_real'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'cifake_fake'), exist_ok=True)

# 1. Extract subset from Celeb-DF
print("Extracting from Celeb-DF...")
try:
    with zipfile.ZipFile(celeb_zip_path, 'r') as z:
        all_files = z.namelist()
        real_vids = [f for f in all_files if f.startswith('Celeb-real/') and f.endswith('.mp4')]
        fake_vids = [f for f in all_files if f.startswith('Celeb-synthesis/') and f.endswith('.mp4')]
        
        print(f"Found {len(real_vids)} real and {len(fake_vids)} fake videos.")
        
        # Select a subset (e.g., 50 new ones)
        # Avoid the first few that might already be extracted (id0_)
        subset_real = [f for f in real_vids if 'id2_' in f or 'id3_' in f or 'id4_' in f][:50]
        subset_fake = [f for f in fake_vids if 'id2_' in f or 'id3_' in f or 'id4_' in f][:50]
        
        for f in subset_real:
            z.extract(f, output_dir)
            os.rename(os.path.join(output_dir, f), os.path.join(output_dir, 'real', os.path.basename(f)))
        
        for f in subset_fake:
            z.extract(f, output_dir)
            os.rename(os.path.join(output_dir, f), os.path.join(output_dir, 'fake', os.path.basename(f)))
            
        # Clean up empty extracted dirs if any
        if os.path.exists(os.path.join(output_dir, 'Celeb-real')):
            os.rmdir(os.path.join(output_dir, 'Celeb-real'))
        if os.path.exists(os.path.join(output_dir, 'Celeb-synthesis')):
            os.rmdir(os.path.join(output_dir, 'Celeb-synthesis'))
            
    print("Celeb-DF extraction done.")
except Exception as e:
    print(f"Error extracting Celeb-DF: {e}")

# 2. Extract subset from CIFAKE
print("Extracting from CIFAKE...")
try:
    with zipfile.ZipFile(cifake_zip_path, 'r') as z:
        all_files = z.namelist()
        c_real = [f for f in all_files if 'REAL' in f and f.endswith('.jpg')]
        c_fake = [f for f in all_files if 'FAKE' in f and f.endswith('.jpg')]
        
        print(f"Found {len(c_real)} real and {len(c_fake)} fake images in CIFAKE.")
        
        subset_creal = c_real[:100]
        subset_cfake = c_fake[:100]
        
        for f in subset_creal:
            z.extract(f, output_dir)
            # Flatten path
            os.rename(os.path.join(output_dir, f), os.path.join(output_dir, 'cifake_real', os.path.basename(f)))
            
        for f in subset_cfake:
            z.extract(f, output_dir)
            os.rename(os.path.join(output_dir, f), os.path.join(output_dir, 'cifake_fake', os.path.basename(f)))
            
    print("CIFAKE extraction done.")
except Exception as e:
    print(f"Error extracting CIFAKE: {e}")

print("All extraction complete.")
