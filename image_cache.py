from PIL import Image, ImageTk

class ImageCache:
    def __init__(self):
        self.cache = {}
        
    def get_image(self, path, size=(800, 600)):
        """
        Get an image from cache or load it if not cached
        
        Args:
            path: Path to the image file
            size: Tuple of (width, height) for resizing
            
        Returns:
            ImageTk.PhotoImage object
        """
        cache_key = f"{path}_{size[0]}x{size[1]}"
        
        if cache_key not in self.cache:
            try:
                img = Image.open(path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.cache[cache_key] = img_tk
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                return None
                
        return self.cache[cache_key]
        
    def clear(self):
        """Clear the image cache"""
        self.cache.clear()
        
    def remove(self, path, size=(800, 600)):
        """Remove a specific image from cache"""
        cache_key = f"{path}_{size[0]}x{size[1]}"
        if cache_key in self.cache:
            del self.cache[cache_key]
