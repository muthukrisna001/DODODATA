import requests
import json
import base64
import io
import hashlib
import os
import logging
from datetime import datetime
from urllib.parse import quote

logger = logging.getLogger(__name__)

class AIImageGenerator:
    """
    AI Image Generator using free open-source APIs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Create directory for generated images
        self.images_dir = os.path.join('static', 'generated_images')
        os.makedirs(self.images_dir, exist_ok=True)
    
    def generate_images(self, prompt, num_images=6):
        """
        Generate images using free AI image generation APIs
        """
        generated_images = []

        # Use Pollinations.ai as primary generator (most reliable)
        pollinations_images = self.generate_with_pollinations(prompt, num_images)
        generated_images.extend(pollinations_images)

        # If we need more images, add variations
        if len(generated_images) < num_images:
            remaining = num_images - len(generated_images)
            variation_images = self.generate_variations(prompt, remaining)
            generated_images.extend(variation_images)

        return generated_images[:num_images]
    
    def generate_with_pollinations(self, prompt, num_images=3):
        """
        Generate images using Pollinations.ai (free Stable Diffusion API)
        """
        try:
            images = []
            
            # Enhance the prompt for better results
            enhanced_prompt = self.enhance_prompt(prompt)
            
            for i in range(num_images):
                # Add variation to each image
                varied_prompt = f"{enhanced_prompt}, variation {i+1}, high quality, detailed"
                
                # Create unique seed for each image
                seed = abs(hash(f"{prompt}_{i}")) % 1000000
                
                # Pollinations.ai API endpoint (simplified)
                url = f"https://image.pollinations.ai/prompt/{quote(varied_prompt)}?seed={seed}&width=512&height=512"
                
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        # Save image locally
                        image_filename = f"pollinations_{hashlib.md5(f'{prompt}_{i}'.encode()).hexdigest()}.jpg"
                        image_path = os.path.join(self.images_dir, image_filename)
                        
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        images.append({
                            'url': f"/static/generated_images/{image_filename}",
                            'thumbnail': f"/static/generated_images/{image_filename}",
                            'title': f"AI Generated: {prompt}",
                            'source': 'Pollinations.ai (Stable Diffusion)',
                            'source_url': url,
                            'author': 'AI Generated',
                            'width': 512,
                            'height': 512,
                            'prompt': varied_prompt
                        })
                        
                except Exception as e:
                    logger.debug(f"Error generating image {i} with Pollinations: {str(e)}")
                    continue
            
            return images
            
        except Exception as e:
            logger.error(f"Error with Pollinations API: {str(e)}")
            return []
    
    def generate_with_huggingface(self, prompt, num_images=2):
        """
        Generate images using Hugging Face free inference API
        """
        try:
            images = []
            
            # Hugging Face models that are free to use
            models = [
                "runwayml/stable-diffusion-v1-5",
                "stabilityai/stable-diffusion-2-1"
            ]
            
            enhanced_prompt = self.enhance_prompt(prompt)
            
            for i, model in enumerate(models[:num_images]):
                try:
                    # Hugging Face Inference API
                    api_url = f"https://api-inference.huggingface.co/models/{model}"
                    
                    payload = {
                        "inputs": enhanced_prompt,
                        "parameters": {
                            "num_inference_steps": 20,
                            "guidance_scale": 7.5,
                            "width": 512,
                            "height": 512
                        }
                    }
                    
                    response = self.session.post(api_url, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        # Save image locally
                        image_filename = f"huggingface_{hashlib.md5(f'{prompt}_{model}'.encode()).hexdigest()}.jpg"
                        image_path = os.path.join(self.images_dir, image_filename)
                        
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        images.append({
                            'url': f"/static/generated_images/{image_filename}",
                            'thumbnail': f"/static/generated_images/{image_filename}",
                            'title': f"AI Generated: {prompt}",
                            'source': f'Hugging Face ({model.split("/")[-1]})',
                            'source_url': f"https://huggingface.co/{model}",
                            'author': 'AI Generated',
                            'width': 512,
                            'height': 512,
                            'prompt': enhanced_prompt
                        })
                        
                except Exception as e:
                    logger.debug(f"Error with Hugging Face model {model}: {str(e)}")
                    continue
            
            return images
            
        except Exception as e:
            logger.error(f"Error with Hugging Face API: {str(e)}")
            return []
    
    def generate_variations(self, prompt, num_images=2):
        """
        Generate variations using different prompt styles
        """
        try:
            images = []
            
            # Different artistic styles to apply
            styles = [
                "photorealistic, high detail, 4k",
                "digital art, vibrant colors, artistic",
                "oil painting style, classical art",
                "watercolor painting, soft colors",
                "pencil sketch, black and white",
                "anime style, manga art"
            ]
            
            for i in range(num_images):
                style = styles[i % len(styles)]
                styled_prompt = f"{prompt}, {style}"
                
                # Use Pollinations with different styles
                seed = abs(hash(f"{styled_prompt}_{i}")) % 1000000
                url = f"https://image.pollinations.ai/prompt/{quote(styled_prompt)}?seed={seed}&width=512&height=512"
                
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        # Save image locally
                        image_filename = f"variation_{hashlib.md5(f'{styled_prompt}_{i}'.encode()).hexdigest()}.jpg"
                        image_path = os.path.join(self.images_dir, image_filename)
                        
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        images.append({
                            'url': f"/static/generated_images/{image_filename}",
                            'thumbnail': f"/static/generated_images/{image_filename}",
                            'title': f"AI Generated: {prompt} ({style.split(',')[0]})",
                            'source': 'AI Variation Generator',
                            'source_url': url,
                            'author': 'AI Generated',
                            'width': 512,
                            'height': 512,
                            'prompt': styled_prompt
                        })
                        
                except Exception as e:
                    logger.debug(f"Error generating variation {i}: {str(e)}")
                    continue
            
            return images
            
        except Exception as e:
            logger.error(f"Error generating variations: {str(e)}")
            return []
    
    def enhance_prompt(self, prompt):
        """
        Enhance the user prompt for better AI generation results
        """
        # Add quality enhancers
        quality_terms = "high quality, detailed, professional, masterpiece"
        
        # Clean and enhance the prompt
        enhanced = f"{prompt}, {quality_terms}"
        
        # Remove any potentially problematic terms
        enhanced = enhanced.replace("NSFW", "").replace("explicit", "")
        
        return enhanced.strip()
