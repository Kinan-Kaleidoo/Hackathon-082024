from PIL import Image
from io import BytesIO
import requests
from fractions import Fraction



def extract_image_info(img):
    try:
        # Get image information
        info = {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "format_description": img.format_description,
            "is_animated": getattr(img, 'is_animated', False),
            "palette": img.getpalette() if img.mode == 'P' else None,
            "transparency": img.gettransparency() if img.info.get('transparency') is not None else None,
        }
        
        # Ensure DPI is JSON serializable
        
      
        return info
    except Exception as e:
        print(f"Error processing image: {e}")
        return {}
