import logging
from .wikidata_service import WikidataService

logger = logging.getLogger(__name__)

class FactsService:
    """
    Service to get IT/AI facts using only Wikidata API
    """

    def __init__(self):
        self.wikidata_service = WikidataService()

    def get_extinct_fact(self):
        """
        Get an IT/AI fact from Wikidata
        """
        try:
            # Get fact from Wikidata
            fact_data = self.wikidata_service.get_it_ai_fact()

            if fact_data:
                return fact_data
            else:
                # Fallback to curated facts if Wikidata fails
                return self.wikidata_service.get_fallback_it_ai_fact()

        except Exception as e:
            logger.error(f"Error getting IT/AI fact: {str(e)}")
            # Return fallback fact on any error
            return self.wikidata_service.get_fallback_it_ai_fact()
