#!/usr/bin/env python3
"""
Voice Extractor - Extract voice profiles from blog content

Usage:
    python main.py <blog-url> --name <voice-name> [--articles N]

Example:
    python main.py https://medium.com/@user --name my-blog --articles 10
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from scraper import BlogScraper
    from analyzer import VoiceAnalyzer
except ImportError:
    print("Error: Could not import scraper/analyzer modules")
    print("Make sure you're running from the voice_extractor directory")
    sys.exit(1)

def _save_articles_for_claude_code(articles, voice_name: str) -> Path:
    """Save scraped articles to a combined file for manual analysis with Claude Code."""
    output_dir = Path("../working")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"scraped-articles-{voice_name}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Scraped Articles for Voice Profile: {voice_name}\n\n")
        f.write(f"Total articles: {len(articles)}\n\n")
        f.write("---\n\n")
        for i, article in enumerate(articles, 1):
            f.write(f"## Article {i}: {article['title']}\n\n")
            f.write(f"{article['content']}\n\n")
            f.write("---\n\n")

    return output_path


def _prompt_for_api_key(articles, voice_name: str):
    """
    Present options when ANTHROPIC_API_KEY is not set.

    Returns the API key string if the user provides one (option 1),
    or None if the user chose option 2 or 3 (both exit the workflow).
    """
    print(f"{'='*60}")
    print("ANTHROPIC_API_KEY is not set")
    print(f"{'='*60}\n")
    print("The voice analyzer requires an Anthropic API key to call")
    print("Claude for voice profile generation.\n")
    print("Choose an option:\n")
    print("  1) Enter your API key now")
    print("  2) Set it as an environment variable (show instructions)")
    print("  3) Skip analysis and use Claude Code instead")
    print()

    while True:
        choice = input("Enter choice [1/2/3]: ").strip()

        if choice == "1":
            print()
            api_key = input("Paste your Anthropic API key: ").strip()
            if not api_key:
                print("\n❌ No key entered. Aborting.\n")
                sys.exit(1)
            print()
            return api_key

        elif choice == "2":
            print(f"\n{'='*60}")
            print("Set your API key, then re-run this command:")
            print(f"{'='*60}\n")
            print("  Linux / macOS:")
            print("    export ANTHROPIC_API_KEY='sk-ant-...'")
            print()
            print("  Windows (Command Prompt):")
            print("    set ANTHROPIC_API_KEY=sk-ant-...")
            print()
            print("  Windows (PowerShell):")
            print('    $env:ANTHROPIC_API_KEY="sk-ant-..."')
            print()
            print("Then re-run:")
            print(f"    python main.py <url> --name {voice_name}\n")
            return None

        elif choice == "3":
            print("\n💾 Saving scraped articles for Claude Code analysis...\n")
            output_path = _save_articles_for_claude_code(articles, voice_name)
            print(f"✅ Articles saved to: {output_path}\n")
            print(f"{'='*60}")
            print("How to generate the voice profile with Claude Code:")
            print(f"{'='*60}\n")
            print("  1. Open Claude Code in the BlogProductionSystem directory")
            print(f"  2. Run:  @orchestrator start")
            print(f"     Or ask Claude Code directly:")
            print(f'     "Read {output_path} and generate a voice profile')
            print(f'      for \'{voice_name}\'. Save it to my-voice/{voice_name}.md"')
            print()
            print("  Claude Code will analyze the articles and create the")
            print("  voice profile without needing an API key.\n")
            return None

        else:
            print("  Invalid choice. Please enter 1, 2, or 3.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract voice profile from blog content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://medium.com/@username --name my-blog
  python main.py https://yourblog.com --name tech-voice --articles 12
        """
    )

    parser.add_argument("url", help="Blog URL to analyze")
    parser.add_argument("--name", required=True, help="Name for this voice profile")
    parser.add_argument("--articles", type=int, default=10,
                       help="Number of articles to analyze (default: 10)")
    parser.add_argument("--save-examples", action="store_true",
                       help="Save scraped articles as examples")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Voice Extractor")
    print(f"{'='*60}\n")

    print(f"📍 Target: {args.url}")
    print(f"🏷️  Voice: {args.name}")
    print(f"📊 Articles: {args.articles}\n")

    # Initialize scraper
    print("🔍 Discovering articles...")
    scraper = BlogScraper(args.url, max_articles=args.articles)

    try:
        articles = scraper.scrape()
    except Exception as e:
        print(f"\n❌ Error scraping articles: {e}")
        sys.exit(1)

    if not articles:
        print("❌ No articles found. Please check the URL and try again.")
        sys.exit(1)

    print(f"✅ Scraped {len(articles)} articles")
    total_words = sum(a.get('word_count', 0) for a in articles)
    print(f"📝 Total words: {total_words:,}\n")

    # Save examples if requested
    if args.save_examples:
        print("💾 Saving article examples...")
        examples_dir = Path(f"../my-voice/examples/{args.name}")
        scraper.save_examples(articles, examples_dir)
        print(f"✅ Examples saved to: {examples_dir}\n")

    # Check for API key before analysis
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        api_key = _prompt_for_api_key(articles, args.name)
        if api_key is None:
            # User chose option 2 (set env var) or option 3 (use Claude Code)
            # Both paths handle their own output and exit
            return

    # Analyze voice
    print("🤖 Analyzing voice patterns with Claude Sonnet 4.5...")
    print("   (This may take 1-2 minutes...)\n")

    analyzer = VoiceAnalyzer(api_key=api_key)

    try:
        profile = analyzer.analyze(articles, voice_name=args.name)
    except Exception as e:
        print(f"\n❌ Error analyzing voice: {e}")
        sys.exit(1)

    # Save profile
    profile_path = Path(f"../my-voice/{args.name}.md")
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(profile)

    print(f"✅ Voice profile created!\n")
    print(f"{'='*60}")
    print(f"📄 Profile: {profile_path}")
    if args.save_examples:
        print(f"📂 Examples: my-voice/examples/{args.name}/")
    print(f"{'='*60}\n")

    print("✨ Ready to use this voice in production!")
    print(f"\nNext steps:")
    print(f"1. Review {profile_path}")
    print(f"2. Edit if needed (especially 'What to AVOID' section)")
    print(f"3. Start production: @orchestrator start\n")

if __name__ == "__main__":
    main()
