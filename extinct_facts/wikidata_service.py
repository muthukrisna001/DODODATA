import requests
import random
import logging

logger = logging.getLogger(__name__)

class WikidataService:
    def __init__(self):
        self.base_url = "https://query.wikidata.org/sparql"
        self.headers = {
            'User-Agent': 'ITAIFactsApp/1.0 (https://example.com/contact)'
        }
        # Track recent facts to avoid repetition
        self.recent_facts = []
        self.max_recent = 5
    
    def get_it_ai_fact(self):
        """
        Get a random IT/AI fact with improved variety
        """
        try:
            # Use fallback facts for reliability
            return self.get_fallback_it_ai_fact()
        except Exception as e:
            logger.error(f"Error getting IT/AI fact: {str(e)}")
            return self.get_fallback_it_ai_fact()
    
    def _add_to_recent(self, title):
        """Add title to recent facts list"""
        if title:
            self.recent_facts.append(title)
            if len(self.recent_facts) > self.max_recent:
                self.recent_facts.pop(0)
    
    def get_fallback_it_ai_fact(self):
        """Get a random IT/AI fact from curated collection"""
        # Combine all fact categories
        all_facts = (
            self._get_programming_language_facts() +
            self._get_computer_scientist_facts() +
            self._get_ai_technology_facts() +
            self._get_software_company_facts() +
            self._get_computing_milestone_facts()
        )
        
        # Try up to 10 times to get a fact we haven't shown recently
        for attempt in range(10):
            fact = random.choice(all_facts)
            if fact.get('title') not in self.recent_facts:
                self._add_to_recent(fact.get('title'))
                return fact
        
        # If all attempts were recent facts, just return a random one
        return random.choice(all_facts)
    
    def _get_programming_language_facts(self):
        """Return facts about programming languages"""
        return [
            {
                "title": "💻 Python Programming Language",
                "description": "Python was created by Guido van Rossum and first released in 1991. Named after the British comedy group Monty Python, it emphasizes code readability and simplicity. Python has become one of the most popular programming languages, especially in data science, AI, and web development. Its philosophy includes 'The Zen of Python' with principles like 'Beautiful is better than ugly' and 'Simple is better than complex'.",
                "image_suggestion": "Python programming language logo code"
            },
            {
                "title": "☕ Java Programming Language",
                "description": "Java was developed by James Gosling at Sun Microsystems and released in 1995. Originally called Oak, it was designed with the principle 'write once, run anywhere' (WORA). Java revolutionized programming with its platform independence through the Java Virtual Machine. It remains one of the most widely used programming languages in enterprise applications and Android development.",
                "image_suggestion": "Java programming language coffee cup logo"
            },
            {
                "title": "🌐 JavaScript",
                "description": "JavaScript was created by Brendan Eich in just 10 days in 1995 while working at Netscape. Despite its name, it has no relation to Java. Originally designed to make web pages interactive, JavaScript has evolved to become a full-stack programming language. It's now used for web development, mobile apps, desktop applications, and even server-side programming with Node.js.",
                "image_suggestion": "JavaScript code on computer screen"
            },
            {
                "title": "🔧 C Programming Language",
                "description": "C was developed by Dennis Ritchie at Bell Labs between 1969 and 1973. It's considered the foundation of modern programming languages, with many languages like C++, Java, and Python borrowing concepts from C. The famous book 'The C Programming Language' by Kernighan and Ritchie is often called the 'K&R' and is considered the bible of C programming. C is still widely used in system programming and embedded systems.",
                "image_suggestion": "C programming language vintage computer terminal"
            },
            {
                "title": "🦀 Rust Programming Language",
                "description": "Rust was originally developed by Mozilla Research, with the first stable release in 2015. It focuses on safety, speed, and concurrency without a garbage collector. Rust prevents common programming errors like null pointer dereferences and buffer overflows at compile time. It's increasingly used in system programming, web assembly, and blockchain development. The language mascot is Ferris the Crab.",
                "image_suggestion": "Rust programming language crab mascot"
            }
        ]
    
    def _get_computer_scientist_facts(self):
        """Return facts about famous computer scientists"""
        return [
            {
                "title": "🧠 Alan Turing",
                "description": "Alan Turing (1912-1954) is considered the father of computer science and artificial intelligence. He created the Turing Test to determine if a machine can exhibit intelligent behavior equivalent to a human. During WWII, he helped break the Enigma code, significantly shortening the war. The Turing Award, often called the 'Nobel Prize of Computing,' is named in his honor. His work laid the theoretical foundation for modern computers.",
                "image_suggestion": "Alan Turing portrait with Enigma machine"
            },
            {
                "title": "👩‍💻 Ada Lovelace",
                "description": "Ada Lovelace (1815-1852) is often considered the world's first computer programmer. She wrote the first algorithm intended to be processed by Charles Babbage's Analytical Engine in 1843. Her notes on the engine include what is recognized as the first computer program. She envisioned that computers could go beyond pure calculation to create music and art. The Ada programming language is named in her honor.",
                "image_suggestion": "Ada Lovelace portrait with mathematical equations"
            },
            {
                "title": "🖥️ Steve Jobs",
                "description": "Steve Jobs (1955-2011) co-founded Apple Inc. and revolutionized personal computing, mobile phones, and digital media. He introduced the Apple II, Macintosh, iPod, iPhone, and iPad, each transforming their respective industries. Known for his perfectionism and attention to design, Jobs believed in making technology accessible and beautiful. His famous Stanford commencement speech included the phrase 'Stay hungry, stay foolish.'",
                "image_suggestion": "Steve Jobs presenting iPhone on stage"
            },
            {
                "title": "🌐 Tim Berners-Lee",
                "description": "Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN. He created the first web browser, web server, and website. Remarkably, he chose not to patent his invention, believing the web should be free for everyone. He founded the World Wide Web Consortium (W3C) to oversee the web's development. He continues to advocate for an open, decentralized web and digital rights.",
                "image_suggestion": "Tim Berners-Lee with early web browser"
            },
            {
                "title": "🔍 Larry Page & Sergey Brin",
                "description": "Larry Page and Sergey Brin co-founded Google in 1998 while PhD students at Stanford University. They developed the PageRank algorithm that became the foundation of Google's search engine. Their innovation was ranking web pages based on their relevance and authority rather than just keyword matching. Google started in a garage and grew to become one of the world's most valuable companies, revolutionizing how we access information.",
                "image_suggestion": "Google founders Larry Page Sergey Brin early office"
            }
        ]

    def _get_ai_technology_facts(self):
        """Return facts about AI technologies"""
        return [
            {
                "title": "🤖 ChatGPT",
                "description": "ChatGPT was released by OpenAI in November 2022 and became the fastest-growing consumer application in history, reaching 100 million users in just 2 months. It's based on the GPT (Generative Pre-trained Transformer) architecture and can engage in human-like conversations, write code, create content, and solve problems. The technology represents a breakthrough in natural language processing and has sparked widespread discussion about AI's role in society.",
                "image_suggestion": "ChatGPT interface conversation artificial intelligence"
            },
            {
                "title": "🧠 Neural Networks",
                "description": "Artificial neural networks are inspired by biological neural networks in animal brains. The concept was first introduced in 1943 by Warren McCulloch and Walter Pitts. Modern deep learning neural networks can have millions or billions of parameters and are used in image recognition, natural language processing, and game playing. The 2024 Nobel Prize in Physics was awarded to Geoffrey Hinton and John Hopfield for their foundational work on neural networks.",
                "image_suggestion": "Neural network diagram brain connections"
            },
            {
                "title": "🎯 Machine Learning",
                "description": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. The term was coined by Arthur Samuel in 1959. ML algorithms can identify patterns in data and make predictions or decisions. Applications include recommendation systems (Netflix, Spotify), fraud detection, medical diagnosis, and autonomous vehicles. The field has exploded with the availability of big data and powerful computing.",
                "image_suggestion": "Machine learning algorithms data visualization"
            },
            {
                "title": "👁️ Computer Vision",
                "description": "Computer Vision enables machines to interpret and understand visual information from the world. Early work began in the 1960s, but modern computer vision uses deep learning to achieve human-level performance in many tasks. Applications include facial recognition, medical imaging, autonomous vehicles, and augmented reality. The ImageNet competition, started in 2010, significantly advanced the field by providing large datasets for training.",
                "image_suggestion": "Computer vision image recognition technology"
            },
            {
                "title": "🗣️ Natural Language Processing",
                "description": "Natural Language Processing (NLP) combines computational linguistics with machine learning to help computers understand human language. Early NLP systems were rule-based, but modern systems use statistical and neural approaches. Breakthrough applications include machine translation (Google Translate), voice assistants (Siri, Alexa), and text generation. The Transformer architecture, introduced in 2017, revolutionized NLP and led to models like GPT and BERT.",
                "image_suggestion": "Natural language processing text analysis"
            }
        ]

    def _get_software_company_facts(self):
        """Return facts about major software companies"""
        return [
            {
                "title": "🏢 Microsoft Corporation",
                "description": "Microsoft was founded by Bill Gates and Paul Allen in 1975, starting in a garage in Albuquerque, New Mexico. The company revolutionized personal computing with MS-DOS and Windows operating systems. Microsoft Office became the standard for productivity software. Under Satya Nadella's leadership since 2014, Microsoft has transformed into a cloud-first company with Azure becoming a major competitor to Amazon Web Services.",
                "image_suggestion": "Microsoft headquarters campus Redmond Washington"
            },
            {
                "title": "🍎 Apple Inc.",
                "description": "Apple was founded in 1976 by Steve Jobs, Steve Wozniak, and Ronald Wayne in Jobs' parents' garage. The company introduced the Apple II, one of the first successful personal computers. After Jobs returned in 1997, Apple launched revolutionary products: iMac, iPod, iPhone, and iPad. Apple became the world's most valuable company and changed multiple industries including computers, music, phones, and tablets.",
                "image_suggestion": "Apple Park headquarters Cupertino California"
            },
            {
                "title": "🔍 Google (Alphabet)",
                "description": "Google was founded in 1998 by Larry Page and Sergey Brin while they were PhD students at Stanford. Starting as a search engine, Google now dominates web search with over 90% market share. The company expanded into email (Gmail), mobile operating systems (Android), cloud computing, and artificial intelligence. Google's parent company Alphabet was created in 2015 to organize its various businesses.",
                "image_suggestion": "Google headquarters Mountain View California colorful"
            }
        ]

    def _get_computing_milestone_facts(self):
        """Return facts about major computing milestones"""
        return [
            {
                "title": "💾 The First Computer Bug",
                "description": "The term 'computer bug' originated in 1947 when Admiral Grace Hopper found an actual moth trapped in a Harvard Mark II computer, causing it to malfunction. She taped the moth in her logbook with the note 'First actual case of bug being found.' This incident popularized the terms 'bug' and 'debugging' in computing. Grace Hopper was also instrumental in developing the first compiler and the COBOL programming language.",
                "image_suggestion": "Grace Hopper computer bug moth logbook"
            },
            {
                "title": "🌐 The First Website",
                "description": "The world's first website was created by Tim Berners-Lee in 1991 at CERN. The site, info.cern.ch, explained what the World Wide Web was and how to use it. It contained information about hypertext, technical details, and how to create web pages. The site is still online today and represents the humble beginning of the web that now contains billions of pages.",
                "image_suggestion": "First website CERN Tim Berners-Lee 1991"
            },
            {
                "title": "📧 The First Email",
                "description": "The first email was sent by Ray Tomlinson in 1971 between two computers sitting side by side. He chose the @ symbol to separate the user name from the computer name, a convention still used today. The message was a test and likely said something like 'QWERTYUIOP.' This simple innovation revolutionized communication and laid the foundation for modern digital messaging.",
                "image_suggestion": "Ray Tomlinson first email 1971 computer terminal"
            }
        ]
