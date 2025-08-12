# DJI Drone Image Metadata Angle Fix

Fixes cases where the gimbal roll metadata is incorrectly set to 180 (should < 180) in DJI drone images.

## Usage

```bash
pip install -r requirements.txt
python fix_angle.py /path/to/images
```

The script recursively processes all JPG files in the specified directory.
