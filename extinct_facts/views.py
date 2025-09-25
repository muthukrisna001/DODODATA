from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import logging
import requests
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

from .facts_service import FactsService

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    """
    Render the main page with the extinct facts button
    """
    return render(request, 'extinct_facts/index.html')

@api_view(['POST'])
def get_extinct_fact(request):
    """
    API endpoint to get an extinct fact with variety tracking
    """
    try:
        facts_service = FactsService()

        # Get recently shown facts from session to avoid immediate repetition
        if not request.session.session_key:
            request.session.create()

        recent_facts = request.session.get('recent_facts', [])

        # Try to get a new fact (with some attempts to avoid repetition)
        max_attempts = 10
        for attempt in range(max_attempts):
            fact_data = facts_service.get_extinct_fact()

            # Ensure we have a proper response format
            if not isinstance(fact_data, dict):
                fact_data = {
                    "title": "Extinct Fact",
                    "description": str(fact_data),
                    "image_suggestion": "Prehistoric scene"
                }

            # Check if this fact was recently shown
            fact_title = fact_data.get('title', '')
            if fact_title not in recent_facts or attempt == max_attempts - 1:
                # Add to recent facts (keep only last 5)
                recent_facts.append(fact_title)
                if len(recent_facts) > 5:
                    recent_facts = recent_facts[-5:]
                request.session['recent_facts'] = recent_facts
                request.session.modified = True
                break

        return Response(fact_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in get_extinct_fact view: {str(e)}")
        return Response(
            {
                "title": "Error",
                "description": "Sorry, we couldn't fetch an extinct fact right now. Please try again later.",
                "image_suggestion": "Error icon"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def get_latest_news(request):
    """
    API endpoint to get latest tech/AI news from multiple sources
    """
    try:
        # Get recently shown news from session to avoid immediate repetition
        if not request.session.session_key:
            request.session.create()

        recent_news = request.session.get('recent_news', [])

        # Try to fetch fresh news from multiple sources
        news_data = fetch_tech_news(recent_news)

        if news_data:
            # Add to recent news (keep only last 10)
            news_title = news_data.get('title', '')
            recent_news.append(news_title)
            if len(recent_news) > 10:
                recent_news = recent_news[-10:]
            request.session['recent_news'] = recent_news
            request.session.modified = True

            return Response(news_data, status=status.HTTP_200_OK)
        else:
            # Fallback to curated news if fetching fails
            return get_fallback_news(recent_news, request)

    except Exception as e:
        logger.error(f"Error in get_latest_news view: {str(e)}")
        return get_fallback_news([], request)


def fetch_tech_news(recent_news):
    """
    Fetch latest tech news from multiple free sources
    """
    try:
        # Try multiple sources for tech news
        sources = [
            fetch_hacker_news(),
            fetch_github_trending(),
            fetch_dev_to_articles(),
            fetch_it_policy_news(),
        ]

        # Filter out None results and recently shown news
        valid_news = []
        for news in sources:
            if news and news.get('title') not in recent_news:
                valid_news.append(news)

        if valid_news:
            # Return a random article from valid news
            import random
            return random.choice(valid_news)

    except Exception as e:
        logger.error(f"Error fetching tech news: {str(e)}")

    return None


def fetch_hacker_news():
    """
    Fetch latest tech news from Hacker News API
    """
    try:
        # Get top stories from Hacker News
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=5)
        if response.status_code == 200:
            story_ids = response.json()[:10]  # Get top 10 stories

            # Get a random story from top 10
            import random
            story_id = random.choice(story_ids)

            # Fetch story details
            story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', timeout=5)
            if story_response.status_code == 200:
                story = story_response.json()

                # Filter for tech-related stories
                title = story.get('title', '')
                if any(keyword.lower() in title.lower() for keyword in ['AI', 'Python', 'JavaScript', 'React', 'OpenAI', 'Google', 'Microsoft', 'Apple', 'programming', 'developer', 'tech', 'software', 'coding', 'machine learning', 'neural', 'algorithm']):
                    return {
                        'title': f"🔥 {title}",
                        'description': f"Latest from Hacker News: {title}. This story is currently trending among developers and tech professionals worldwide.",
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    }
    except Exception as e:
        logger.error(f"Error fetching Hacker News: {str(e)}")

    return None


def fetch_github_trending():
    """
    Fetch trending repositories from GitHub
    """
    try:
        # GitHub's search API for trending repositories
        today = datetime.now().strftime('%Y-%m-%d')
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        url = f'https://api.github.com/search/repositories?q=created:>{week_ago}&sort=stars&order=desc&per_page=10'
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            repos = response.json().get('items', [])
            if repos:
                import random
                repo = random.choice(repos[:5])  # Pick from top 5

                return {
                    'title': f"⭐ {repo['name']} - Trending on GitHub",
                    'description': f"{repo.get('description', 'A trending repository on GitHub')}. This project has gained {repo['stargazers_count']} stars and is written in {repo.get('language', 'various languages')}.",
                    'url': repo['html_url']
                }
    except Exception as e:
        logger.error(f"Error fetching GitHub trending: {str(e)}")

    return None


def fetch_dev_to_articles():
    """
    Fetch latest articles from Dev.to API
    """
    try:
        # Dev.to API for latest articles
        response = requests.get('https://dev.to/api/articles?tag=javascript,python,ai,react,programming&top=7', timeout=5)

        if response.status_code == 200:
            articles = response.json()
            if articles:
                import random
                article = random.choice(articles[:10])

                return {
                    'title': f"📝 {article['title']}",
                    'description': f"{article.get('description', article['title'])}. Published on Dev.to by {article.get('user', {}).get('name', 'a developer')}.",
                    'url': article['url']
                }
    except Exception as e:
        logger.error(f"Error fetching Dev.to articles: {str(e)}")

    return None


def fetch_it_policy_news():
    """
    Fetch IT policy and industry regulation news
    """
    try:
        # Try to fetch from news APIs for policy-related content
        # Using NewsAPI's free tier or similar services

        # For now, we'll include curated policy news that gets updated
        current_policy_news = [
            {
                'title': "🏛️ H1B Visa Fee Increases Impact Tech Workers",
                'description': "Recent policy changes have increased H1B visa application fees significantly, affecting thousands of IT professionals. The new fee structure includes higher base fees and additional charges for premium processing, impacting both employers and visa applicants in the tech industry.",
                'url': "https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-1b-specialty-occupations"
            },
            {
                'title': "📋 New I-94 Digital Requirements for Tech Professionals",
                'description': "Updated I-94 digital entry requirements now affect how international tech workers track their legal status. The changes include new online verification systems and updated documentation requirements for maintaining legal work status in the US.",
                'url': "https://i94.cbp.dhs.gov/"
            },
            {
                'title': "💼 Remote Work Tax Implications for IT Workers",
                'description': "New tax regulations affect IT professionals working remotely across state lines. Recent IRS guidance clarifies tax obligations for remote workers, particularly impacting software developers and IT consultants working for companies in different states.",
                'url': "https://www.irs.gov/newsroom/faqs-for-individuals-working-remotely"
            },
            {
                'title': "🔒 GDPR Compliance Updates Affect IT Departments",
                'description': "Recent GDPR enforcement actions have resulted in significant fines for tech companies, highlighting the importance of data privacy compliance. IT departments are implementing new protocols to ensure compliance with evolving privacy regulations.",
                'url': "https://gdpr.eu/what-is-gdpr/"
            },
            {
                'title': "⚖️ AI Regulation Bills Impact Software Development",
                'description': "Proposed AI regulation legislation could significantly impact how software developers build and deploy AI systems. The bills include requirements for AI transparency, bias testing, and accountability measures that will affect development workflows.",
                'url': "https://www.congress.gov/search?q=artificial+intelligence"
            },
            {
                'title': "🌐 Net Neutrality Changes Affect Tech Infrastructure",
                'description': "Recent net neutrality policy changes impact how tech companies manage their infrastructure and content delivery. The changes affect bandwidth allocation, content prioritization, and infrastructure investment decisions for IT departments.",
                'url': "https://www.fcc.gov/restoring-internet-freedom"
            },
            {
                'title': "💳 Cryptocurrency Regulation Updates for Tech Companies",
                'description': "New cryptocurrency regulations affect tech companies involved in blockchain development, digital payments, and crypto-related services. The updates include compliance requirements for exchanges, wallet providers, and DeFi platforms.",
                'url': "https://www.sec.gov/spotlight/cybersecurity-enforcement-actions"
            },
            {
                'title': "🏢 Corporate Tax Changes Impact Tech Startups",
                'description': "Recent corporate tax policy changes specifically affect tech startups and software companies. The changes include modifications to R&D tax deductions, startup expense treatments, and international tax obligations for tech businesses.",
                'url': "https://www.irs.gov/businesses/small-businesses-self-employed/business-taxes"
            }
        ]

        # Return a random policy news item
        import random
        return random.choice(current_policy_news)

    except Exception as e:
        logger.error(f"Error fetching IT policy news: {str(e)}")

    return None


def get_fallback_news(recent_news, request):
    """
    Fallback to curated news when APIs fail
    """
    fallback_news = [
        # Technical News
        {
            'title': "🚀 OpenAI Releases GPT-4 Turbo with Vision",
            'description': "OpenAI has announced GPT-4 Turbo, featuring improved performance, lower costs, and the ability to process images alongside text. The new model offers a 128K context window and represents a significant advancement in multimodal AI capabilities.",
            'url': "https://openai.com/blog/gpt-4-turbo"
        },
        {
            'title': "🤖 DeepSeek Releases Open-Source AI Models",
            'description': "DeepSeek has released a series of open-source AI models that rival GPT-4 performance while being freely available. Their DeepSeek-V2 model shows impressive capabilities in coding, mathematics, and reasoning tasks.",
            'url': "https://github.com/deepseek-ai"
        },
        {
            'title': "⚡ Python 3.12 Introduces New Features",
            'description': "Python 3.12 brings significant performance improvements, better error messages, and new syntax features. The release includes enhanced f-string capabilities, improved type hints, and up to 11% faster execution.",
            'url': "https://docs.python.org/3.12/whatsnew/3.12.html"
        },
        {
            'title': "🔧 JavaScript ES2024 Features Released",
            'description': "The latest ECMAScript 2024 specification introduces new array methods, improved regex support, and better async/await handling. Notable additions include Array.prototype.toSorted() and enhanced temporal API support.",
            'url': "https://tc39.es/ecma262/"
        },
        {
            'title': "🌟 GitHub Copilot Gets Major Updates",
            'description': "GitHub Copilot now features improved code suggestions, better context awareness, and support for more programming languages. The AI assistant can now understand larger codebases and provide more accurate suggestions.",
            'url': "https://github.blog/changelog/label/copilot/"
        },
        # Policy & Industry News
        {
            'title': "🏛️ H1B Visa Processing Delays Impact Tech Hiring",
            'description': "Significant delays in H1B visa processing are affecting tech company hiring plans for 2024. Companies are reporting 6-12 month delays in visa approvals, forcing them to reconsider international hiring strategies and remote work arrangements.",
            'url': "https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-1b-specialty-occupations"
        },
        {
            'title': "💼 Remote Work Tax Laws Create Compliance Challenges",
            'description': "New multi-state tax regulations are creating compliance challenges for IT professionals working remotely. Companies are implementing new payroll systems to handle complex tax obligations across different jurisdictions.",
            'url': "https://www.irs.gov/newsroom/faqs-for-individuals-working-remotely"
        },
        {
            'title': "⚖️ EU AI Act Implementation Affects Global Tech Companies",
            'description': "The European Union's AI Act implementation is forcing global tech companies to redesign their AI systems for compliance. The regulations include strict requirements for high-risk AI applications and transparency obligations.",
            'url': "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"
        },
        {
            'title': "🔒 Cybersecurity Regulations Tighten for Financial Tech",
            'description': "New cybersecurity regulations specifically targeting fintech companies require enhanced security measures and incident reporting. IT departments are implementing new security frameworks to meet compliance requirements.",
            'url': "https://www.cisa.gov/cybersecurity"
        },
        {
            'title': "🌐 Data Privacy Laws Expand Globally",
            'description': "New data privacy regulations similar to GDPR are being implemented worldwide, affecting how tech companies handle user data. IT teams are updating privacy policies, data handling procedures, and user consent mechanisms.",
            'url': "https://gdpr.eu/what-is-gdpr/"
        }
    ]

    # Filter out recently shown news
    available_news = [news for news in fallback_news if news['title'] not in recent_news]

    if not available_news:
        # Reset if all news have been shown
        available_news = fallback_news
        request.session['recent_news'] = []

    import random
    selected_news = random.choice(available_news)

    # Update recent news
    recent_news = request.session.get('recent_news', [])
    recent_news.append(selected_news['title'])
    if len(recent_news) > 10:
        recent_news = recent_news[-10:]
    request.session['recent_news'] = recent_news
    request.session.modified = True

    return Response(selected_news, status=status.HTTP_200_OK)


