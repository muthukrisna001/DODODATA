from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import logging
import requests
import hashlib
import os
from django.conf import settings

logger = logging.getLogger(__name__)

def index(request):
    """
    Main page for AI image generation
    """
    return render(request, 'image_search/index_new.html')

@api_view(['POST'])
def search_images(request):
    """
    API endpoint to generate AI images from text prompts
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('query', '').strip()

        if not prompt:
            return Response({
                'error': 'Please provide a prompt for image generation'
            }, status=400)

        logger.info(f"Generating images for prompt: {prompt}")

        # Generate 6 images with variations
        images = []
        for i in range(6):
            # Create unique prompt variations
            variation_prompt = f"{prompt}, high quality, detailed, professional, masterpiece, variation {i+1}"
            
            # Generate unique seed for each image
            seed = hash(f"{prompt}_{i}") % 1000000
            
            # Create Pollinations.ai URL
            pollinations_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(variation_prompt)}?seed={seed}&width=512&height=512"
            
            # Download and save image
            try:
                image_response = requests.get(pollinations_url, timeout=30)
                if image_response.status_code == 200:
                    # Create filename
                    filename_hash = hashlib.md5(f"{prompt}_{i}_{seed}".encode()).hexdigest()
                    filename = f"pollinations_{filename_hash}.jpg"
                    
                    # Ensure static directory exists
                    static_dir = os.path.join(settings.BASE_DIR, 'static', 'generated_images')
                    os.makedirs(static_dir, exist_ok=True)
                    
                    # Save image
                    filepath = os.path.join(static_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(image_response.content)
                    
                    # Add to results
                    images.append({
                        'url': f'/static/generated_images/{filename}',
                        'title': f'AI Generated: {prompt}',
                        'source': 'Pollinations.ai (Stable Diffusion)',
                        'source_url': pollinations_url,
                        'prompt': variation_prompt
                    })
                    
                    logger.info(f"Successfully generated image {i+1}/6")
                else:
                    logger.warning(f"Failed to download image {i+1}: HTTP {image_response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error downloading image {i+1}: {str(e)}")
                continue

        if not images:
            return Response({
                'error': 'Failed to generate any images. Please try again.'
            }, status=500)

        logger.info(f"Successfully generated {len(images)} images")
        
        return Response({
            'query': prompt,
            'total_results': len(images),
            'images': images
        })

    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in search_images: {str(e)}")
        return Response({
            'error': 'An unexpected error occurred. Please try again.'
        }, status=500)
