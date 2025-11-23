# Blog Production System

Automated blog production system powered by Claude Code. Transform concepts into publication-ready content while maintaining authentic voice.

## Overview

This system coordinates specialized AI agents to handle the complete blog workflow:

**Concept** → Research → Structure → Draft → Quality Gates → SEO → **Published Article**

All while preserving your unique voice.

## Features

✅ **Voice-First Production** - Maintains authentic writing style
✅ **Automated Research** - Finds and validates credible sources with automatic fallbacks
✅ **Web Request Resilience** - 30s timeouts prevent hanging, smart failure handling
✅ **Quality Gates** - Ensures voice consistency (9+/10) and citation accuracy
✅ **Flexible Fact-Checking** - Distinguishes permanent vs temporary source failures
✅ **SEO Optimization** - Improves discoverability without breaking voice
✅ **Complete Audit Trail** - Every stage documented and archived

## Quick Start

### 1. Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.8+ (for voice extraction)
- Anthropic API key

### 2. Extract Your Voice Profile

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Extract voice from your blog
cd voice_extractor
pip install -r requirements.txt
python main.py https://your-blog.com --name my-voice --articles 10 --save-examples
```

This analyzes your articles and creates:
- `my-voice/my-voice.md` - Voice profile
- `my-voice/examples/my-voice/*.md` - Example articles

### 3. Review Voice Profile

Edit `my-voice/my-voice.md` to refine:
- Tone characteristics
- Writing patterns
- **"What to AVOID"** section (critical for quality)

### 4. Create Your Brief (Optional)

Choose a template and fill it in:

```bash
# Copy a template
cp concepts/templates/standard-brief.md concepts/briefs/my-topic-brief.md

# Or use metaphor-driven template
cp concepts/templates/metaphor-brief.md concepts/briefs/my-topic-brief.md

# Or challenge-based template
cp concepts/templates/challenge-brief.md concepts/briefs/my-topic-brief.md

# Edit with your concept
```

**Available Templates**:
- `standard-brief.md` - General article structure
- `metaphor-brief.md` - Metaphor-driven narrative
- `challenge-brief.md` - Problem/solution based

### 5. Start Production

In Claude Code:

```
@orchestrator start
```

The orchestrator will:
1. **Voice Selection** - Interactive picker showing available profiles
2. **Brief Input** - Choose from:
   - Load saved brief from `concepts/briefs/`
   - Use a template (standard/metaphor/challenge)
   - Paste brief directly
   - Interactive extraction (Q&A mode)
3. **Mode Selection** - Automated / Interactive / Partial
4. Run complete production workflow
5. Deliver publication-ready article

## System Architecture

### Agent Workflow

```
User Brief
    ↓
[Interrogator] - Extract knowledge
    ↓
[Research Lead] - Validate with sources
    ↓
[Structure Architect] - Design narrative
    ↓
[Voice Writer] - Create draft
    ↓
[Tone Police] ←── Quality Gate (must score 9+/10)
    ↓
[Fact Checker] ←── Quality Gate (zero errors required)
    ↓
[SEO Optimizer] - Optimize discoverability
    ↓
Published Article + Complete Archive
```

### Key Agents

- **Orchestrator** - Coordinates entire workflow
- **Interrogator** - Extracts your unique insights
- **Research Lead** - Finds credible sources
- **Structure Architect** - Designs article flow
- **Voice Writer** - Creates draft in your voice
- **Tone Police** - Checks voice consistency (quality gate)
- **Fact Checker** - Verifies all citations (quality gate)
- **SEO Optimizer** - Optimizes without breaking voice

## Usage Examples

### Full Production with Template

```
@orchestrator start

> Voice: [Select from interactive picker]
> Brief: Use template → standard-brief.md
> Mode: Automated

[System runs complete workflow]

✅ Published: published/your-article.md
```

### Quick Production (Paste Brief)

```
@orchestrator start

> Voice: [Select from interactive picker]
> Brief: Paste directly → [your concept text]
> Mode: Automated

[System runs complete workflow]
```

### Interactive Mode

```
@orchestrator start

> Voice: [Select from interactive picker]
> Brief: Load from concepts/briefs/ → my-topic-brief.md
> Mode: Interactive

[Pause after each stage for review and approval]
```

### Resume In-Progress

```
@orchestrator resume article-slug
```

### Check Status

```
@orchestrator status
```

## Voice Extraction

The voice extractor analyzes your existing content to capture:

- **Core Identity** - Who you are as a writer
- **Tone Characteristics** - Your distinctive voice qualities
- **Writing Style** - Structure, language, patterns
- **What to AVOID** - Patterns you never use (critical)
- **Signature Phrases** - Recognizable expressions

### Example

```bash
python main.py https://medium.com/@yourname \
    --name medium-voice \
    --articles 12 \
    --save-examples
```

Creates profile that captures your authentic style.

## Quality Gates

### Tone Check
**Requirement**: Score 9.0+/10 with zero critical AI-tells

Scans for:
- Generic business jargon
- AI sentence patterns
- Voice inconsistencies
- Tone drift

**Blocks publication if failed**

### Fact Check
**Requirement**: Zero **permanent** failures (flexible for transient issues)

Verifies:
- All URLs work (with 30s timeout)
- Claims match sources
- Attribution accuracy
- Source credibility

**Flexible Quality Gate**:
- ✅ **PASS**: All sources working OR verified during research (70%+ accessible)
- ⚠️ **CONDITIONAL**: Transient failures (sources worked before, temporarily down) - user decides
- ❌ **FAIL**: Permanent failures (sources never worked) or <70% accessible

**Blocks publication only for permanent issues** - temporary website downtime won't stop your workflow

## File Organization

```
.claude/                     # Claude Code configuration
└── commands/
    └── orchestrator.md      # @orchestrator slash command

my-voice/                    # Your voice profiles
├── blog-voice.md
└── examples/
    └── blog-voice/

concepts/                    # Article briefs and templates
├── templates/
│   ├── standard-brief.md    # General article template
│   ├── metaphor-brief.md    # Metaphor-driven template
│   └── challenge-brief.md   # Challenge-based template
└── briefs/
    └── topic-brief.md       # Your saved briefs

working/                     # Active production
├── interrogation-topic.md
├── draft-topic-v1.md
└── ...

archive/                     # Completed artifacts
└── topic/
    └── [all working files]

published/                   # Final articles
├── topic.md
└── PRODUCTION-SUMMARY-TOPIC.md
```

## Research Integration

The system uses a **voice-first** research pattern:

**Correct**:
> I've watched teams optimize for NPS scores, then fail at enterprise scale. [CB Insights data](url) confirms: 42% of startups fail because users love the product but can't buy it.

**Incorrect** (research-first):
> According to CB Insights, 42% of startups fail due to no market need, which demonstrates challenges in product-market fit.

Your observations lead. Research validates.

## Customization

### Multiple Voice Profiles

Create profiles for different contexts:

```bash
python main.py https://tech-blog.com --name technical-voice
python main.py https://business-blog.com --name business-voice
```

Select voice when starting production.

### Voice Templates

Start with `voice-templates/generic.md` for a blank template.

## Best Practices

### For Voice Extraction
- Analyze 8-12 articles minimum
- Choose representative articles
- Edit extracted profile (especially "What to AVOID")
- Add specific signature phrases
- Test with a draft before full production

### For Brief Creation
- **Use templates** - Start with standard/metaphor/challenge template
- **Be specific** - More context = better output
- **Include examples** - Real scenarios make stronger articles
- **Voice target** - Specify which voice profile to use in brief
- **Save briefs** - Keep in `concepts/briefs/` for reuse and reference

### For Production
- **First time**: Use interactive mode to see each stage
- **Template workflow**: Copy template → fill in → save to briefs/ → @orchestrator start
- **Quick workflow**: @orchestrator start → paste directly
- Review quality gate reports when they fail
- Don't compromise voice for SEO

### For Quality
- Take time on voice profile "What to AVOID" section
- Let quality gates block publication (they're protecting your brand)
- Review archived artifacts to improve future briefs

## Troubleshooting

### Voice Extraction Fails
- Check `ANTHROPIC_API_KEY` is set
- Verify blog URL is accessible
- Try different article count (8-15 optimal)

### Production Quality Gates Fail

**Tone Check < 9.0**:
- Review tone-police report for specific AI-tells
- Check draft against voice profile "What to AVOID"
- Regenerate or manually edit

**Fact Check Errors**:
- Check if failures are PERMANENT (never worked) or TRANSIENT (worked before)
- PERMANENT: Fix broken citations or find replacements
- TRANSIENT: Decide whether to proceed with warnings, wait, or find alternatives
- Verify claims match source content for accessible sources

### Web Research Issues

**Sources Timing Out**:
- System uses 30s timeout - slow sites marked unavailable
- Research-lead finds fallback sources automatically
- Check source availability report in research validation output

**Sites Temporarily Down**:
- TRANSIENT failures noted but don't block publication
- At least 70% of citations must remain accessible
- User decides whether to proceed with conditional approval

### General Issues
- Ensure voice profile exists: `my-voice/{name}.md`
- Check working directory is clean
- Review CLAUDE.md for system documentation

## Requirements

### For Voice Extraction
- Python 3.8+
- `pip install -r voice_extractor/requirements.txt`
- ANTHROPIC_API_KEY environment variable

### For Production
- Claude Code
- Voice profile in `my-voice/`
- No other dependencies

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome. Please:
- Test with multiple voice profiles
- Maintain voice-agnostic approach
- Document configuration options

## Acknowledgments

Built on Claude Code agent system.
Powered by Claude Sonnet 4.5.

---

**Note**: This is an agent system for Claude Code, not a standalone application.
