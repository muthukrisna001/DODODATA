from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import logging

from .ai_image_generator import AIImageGenerator

logger = logging.getLogger(__name__)

def index(request):
    """
    Render the image search page
    """
    return render(request, 'image_search/index.html')

@api_view(['POST'])
def search_images(request):
    """
    API endpoint to generate AI images from text prompts
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('query', '').strip()  # Keep 'query' for frontend compatibility

        if not prompt:
            return Response(
                {'error': 'Prompt parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize AI image generator
        image_generator = AIImageGenerator()

        # Generate images
        images = image_generator.generate_images(prompt, num_images=6)

        return Response({
            'query': prompt,
            'total_results': len(images),
            'images': images
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in generate_images view: {str(e)}")
        return Response(
            {'error': 'Failed to generate images. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
