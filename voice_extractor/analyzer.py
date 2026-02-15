"""
Voice analyzer using Claude API
"""

import os
import anthropic

class VoiceAnalyzer:
    """Analyze articles to extract voice profile"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Pass api_key to VoiceAnalyzer() "
                "or set the ANTHROPIC_API_KEY environment variable."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"  # Sonnet 4.5

    def analyze(self, articles, voice_name: str):
        """Analyze articles and generate voice profile"""

        # Combine articles for analysis
        combined_text = self._combine_articles(articles)

        # Create analysis prompt
        prompt = self._create_prompt(combined_text, voice_name, len(articles))

        # Call Claude
        message = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text

    def _combine_articles(self, articles):
        """Combine articles into single text for analysis"""
        combined = []
        for i, article in enumerate(articles, 1):
            combined.append(f"=== ARTICLE {i}: {article['title']} ===\n\n{article['content']}\n\n")
        return "\n".join(combined)

    def _create_prompt(self, text, voice_name, article_count):
        """Create analysis prompt for Claude"""

        return f"""You are an expert voice and tone analyst. Your task is to analyze the following {article_count} blog articles and create a comprehensive Voice Profile that captures this author's unique writing style.

Analyze the provided articles to identify:
- Core identity and perspective
- Philosophy and worldview
- Tone characteristics
- Writing style patterns
- Content patterns and structures
- Key themes
- Audience relationship
- Voice consistency markers (phrases used and avoided)

Generate a detailed voice profile using this EXACT structure:

---

# Voice Profile: {voice_name}

## Core Identity
[Who is writing? What perspective do they bring? 1-2 sentences.]

## Philosophy
[What is the underlying belief system or worldview driving this writing? 1-2 sentences.]

## Tone Characteristics

### [Characteristic 1]
[Description of this tone quality with examples]

### [Characteristic 2]
[Description of this tone quality with examples]

### [Characteristic 3]
[Description of this tone quality with examples]

[Add more if needed - aim for 3-4 key characteristics]

## Writing Style

### Structure
[How does this author typically structure content? Prose vs bullets? Paragraph length patterns?]

### Opening Strategy
[How do articles typically begin? What hooks does the author use?]

### Language Choices
[Vocabulary level, technical vs accessible, use of metaphors, sentence patterns]

### What to AVOID (CRITICAL)
[This is the most important section - list specific patterns, phrases, and styles this voice NEVER uses]

- [Specific phrase or pattern to avoid]
- [Another pattern to avoid]
- [Generic business jargon this voice doesn't use]
- [Writing structures to avoid]

## Content Patterns

[Describe typical article structures, use of research/citations, recurring frameworks]

## Key Themes

[List 3-4 major recurring topics, arguments, or angles this author explores]

## Audience Relationship

[Who does this content speak to? What's the relationship between author and reader?]

## Voice Consistency Markers

### Signature Phrases
[Phrases this author uses frequently that are recognizable]

- "[Example phrase 1]"
- "[Example phrase 2]"

### Phrases Never Used
[Phrases completely absent from this voice]

- "[Generic phrase this author would never use]"
- "[Another phrase to avoid]"

---

IMPORTANT: Be VERY specific in the "What to AVOID" section. The more specific you are about what this voice doesn't do, the better the output quality will be.

Analyze these {article_count} articles carefully and create the voice profile:

{text}

Generate the complete voice profile now, following the structure above exactly."""
