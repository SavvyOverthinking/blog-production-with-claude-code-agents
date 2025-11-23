# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **blog production system** built on Claude Code agent definitions. It transforms concepts into publication-ready blog posts through an orchestrated multi-agent workflow while maintaining authentic voice.

## Critical Architecture: Agents as Roles, Not Subprocesses

**IMPORTANT**: The agent files in `agents/` are **role definitions for the orchestrator to embody**, not separate Task tool subagents.

When working with this system:
- **DO NOT** invoke agents using `Task` tool with subagent_type like "research-lead" or "voice-writer"
- **INSTEAD**: The orchestrator reads each agent definition and **embodies that role**
- **THEN**: Produces the outputs described in that agent's workflow
- **FINALLY**: Returns to orchestrator role for next stage

### How Agents Work

```
User: "@orchestrator start"

Orchestrator workflow:
1. Asks user for voice, brief, mode
2. Reads agents/interrogator.md
3. BECOMES the interrogator (embodies the role)
4. Executes interrogator's workflow
5. Saves output to working/interrogation-{slug}.md
6. Returns to orchestrator role
7. Reads agents/research-lead.md
8. BECOMES the research-lead
9. Executes research workflow
10. ... continues through all stages
```

## System Requirements

### Voice Profile (REQUIRED)

The system requires a voice profile before use:

**Extract a voice profile**:
```bash
cd voice_extractor
pip install -r requirements.txt
python main.py https://blog-url --name my-voice --articles 10
```

This creates:
- `my-voice/my-voice.md` - Voice profile
- `my-voice/examples/my-voice/*.md` - Example articles

**Voice profiles must include**:
1. Core Identity - Who is writing
2. Philosophy - Core belief driving writing
3. Tone Characteristics - 3-4 specific traits
4. Writing Style - Structure, language, **what to AVOID**
5. Content Patterns - Typical structures
6. Key Themes - Main topics/angles
7. Audience Relationship - Who you're addressing
8. Voice Consistency Markers - Signature phrases

**Critical Section**: "What to AVOID" - The more specific, the better output quality

## Agent Workflow

### Production Orchestrator (`@orchestrator start`)

Main coordinator that embodies each agent role sequentially:

1. **interrogator** - Extracts author's knowledge from brief
2. **research-lead** - Validates with credible sources
3. **structure-architect** - Designs narrative architecture
4. **voice-writer** - Creates draft in authentic voice
5. **tone-police** - Quality gate: voice consistency (must score 9+/10)
6. **fact-checker** - Quality gate: citation verification (must pass)
7. **seo-optimizer** - Optimizes discoverability without breaking voice
8. **final-polish** - Applies safe optimizations
9. **archive-and-publish** - Completes production

### Agent Roles

**interrogator** - Knowledge extraction
- Probes brief for insights
- Maps metaphors if present
- Documents operational details
- Output: `working/interrogation-{slug}.md`

**research-lead** - Source validation
- Finds 3-6 credible sources
- Validates claims
- Prepares citations
- Output: `working/research-validation-{slug}.md`

**structure-architect** - Narrative design
- Identifies structure type (Pattern/Metaphor/Challenge/Mechanism)
- Designs section-by-section blueprint
- Maps research integration
- Output: `working/structure-blueprint-{slug}.md`

**voice-writer** - Draft creation
- Reads voice profile + examples
- Follows structure blueprint
- Integrates research naturally
- Maintains voice throughout
- Output: `working/draft-{slug}-v1.md`

**tone-police** - Voice consistency check
- Scans for AI-tells
- Scores voice consistency (X/10)
- **Quality Gate**: Must score 9.0+ with zero critical AI-tells
- Output: `working/tone-police-report-{slug}.md`

**fact-checker** - Citation verification
- Verifies all URLs work
- Confirms claims match sources
- Checks attribution accuracy
- **Quality Gate**: Must have zero critical issues
- Output: `working/fact-check-report-{slug}.md`

**seo-optimizer** - Discoverability
- Creates title variants
- Writes meta description
- Suggests voice-safe keyword optimizations
- **Rule**: Voice > SEO always
- Output: `working/seo-optimization-{slug}.md`

**editorial-director** - (Optional) Overall quality review
- Can be used for pre-quality-gate review
- Not part of standard automated workflow
- Output: `working/editorial-review-{slug}.md`

## File Organization

```
BlogProductionSystem/
├── .claude/                         # Claude Code configuration
│   └── commands/
│       └── orchestrator.md          # @orchestrator slash command
│
├── agents/                          # Agent role definitions
│   ├── orchestrator.md              # Main coordinator
│   ├── production-manager.md        # Entry point/router
│   ├── interrogator.md              # Knowledge extraction
│   ├── research-lead.md             # Source validation
│   ├── structure-architect.md       # Narrative design
│   ├── voice-writer.md              # Draft creation
│   ├── tone-police.md               # Voice check (quality gate)
│   ├── fact-checker.md              # Citation verification (quality gate)
│   ├── seo-optimizer.md             # SEO without voice compromise
│   └── editorial-director.md        # Optional quality review
│
├── voice_extractor/                 # Python voice extraction tool
│   ├── main.py                      # CLI entry point
│   ├── scraper.py                   # Web scraping
│   ├── analyzer.py                  # LLM voice analysis
│   └── requirements.txt             # Python dependencies
│
├── my-voice/                        # Voice profiles (gitignored)
│   ├── {voice-name}.md              # Voice profile
│   └── examples/
│       └── {voice-name}/*.md        # Example articles
│
├── concepts/                        # Article briefs and templates
│   ├── templates/                   # Brief templates
│   │   ├── standard-brief.md        # General article template
│   │   ├── metaphor-brief.md        # Metaphor-driven template
│   │   └── challenge-brief.md       # Challenge-based template
│   └── briefs/                      # Saved article briefs
│       └── {topic-slug}-brief.md
│
├── working/                         # Active production workspace
│   ├── .state-{slug}.json           # Production state (for resume)
│   ├── interrogation-{slug}.md
│   ├── research-validation-{slug}.md
│   ├── structure-blueprint-{slug}.md
│   ├── draft-{slug}-v1.md
│   ├── tone-police-report-{slug}.md
│   ├── fact-check-report-{slug}.md
│   ├── seo-optimization-{slug}.md
│   └── {slug}-final.md
│
├── archive/                         # Completed production artifacts
│   └── {slug}/
│       └── [all working files]
│
├── published/                       # Final articles
│   ├── {slug}.md
│   └── PRODUCTION-SUMMARY-{SLUG}.md
│
├── voice-templates/                 # Starting voice templates
│   └── generic.md
│
├── .gitignore
├── CLAUDE.md                        # This file
└── README.md                        # User documentation
```

## Typical Workflows

### Full Production from Concept

```
User: "@orchestrator start"

Orchestrator uses AskUserQuestion for setup:
1. Voice Selection - Interactive picker showing available voice profiles
2. Brief Input - Choose from:
   - Load from concepts/briefs/ (saved briefs)
   - Use template (standard/metaphor/challenge)
   - Paste directly
   - Interactive extraction
3. Mode Selection - Automated/Interactive/Partial

Then runs complete workflow:
- Interrogation
- Research
- Structure
- Draft
- Tone check (quality gate)
- Fact check (quality gate)
- SEO optimization
- Final polish
- Publish & archive

Output:
- published/{slug}.md
- archive/{slug}/[all artifacts]
- published/PRODUCTION-SUMMARY-{SLUG}.md
```

### Using Brief Templates

**Standard Article**:
1. Copy `concepts/templates/standard-brief.md`
2. Fill in sections
3. Save to `concepts/briefs/{topic-slug}-brief.md`
4. Run `@orchestrator start` and select "Load from concepts/briefs/"

**Metaphor-Driven Article**:
1. Copy `concepts/templates/metaphor-brief.md`
2. Define core metaphor and mapping
3. Save to `concepts/briefs/{topic-slug}-brief.md`
4. Structure-architect will use metaphor as foundation

**Challenge-Based Article**:
1. Copy `concepts/templates/challenge-brief.md`
2. Describe challenge, failed approaches, solution
3. Save to `concepts/briefs/{topic-slug}-brief.md`
4. Structure-architect will design challenge → solution flow

### Voice Extraction Only

```bash
cd voice_extractor
python main.py https://target-blog.com --name target-voice --articles 10 --save-examples
```

Output:
- `my-voice/target-voice.md`
- `my-voice/examples/target-voice/*.md`

### Resume In-Progress Production

```
User: "@orchestrator resume article-slug"

Orchestrator:
- Loads state from working/.state-article-slug.json
- Shows current progress
- Continues from last checkpoint
```

## Quality Gates (Strict Enforcement)

### Tone Check Gate
**Requirement**: Score 9.0+/10 with zero critical AI-tells

**If FAILED**:
- User must choose: regenerate / manual edit / abort
- Cannot proceed to publication with failing tone check

### Fact Check Gate
**Requirement**: Zero critical issues (no broken links, inaccurate claims, misattributions)

**If FAILED**:
- User must fix issues before proceeding
- Cannot publish with broken citations or false claims

## Voice-Specific Writing Rules

### Research Integration Pattern

**Voice-First Integration** (always):
```
CORRECT:
"I've watched teams with 70+ NPS fail at enterprise.
[CB Insights research](url) validates: 42% of startups fail because they
built for users who love it but can't buy it."

INCORRECT:
"According to CB Insights (2024), 42% of startups fail due to no market
need, demonstrating that user satisfaction doesn't equal viability."
```

### Citation Format
- **Always use inline links**: `[source description](url)`
- **Never use footnotes** or numbered citations
- **Format**: "Organization research reveals..." or "Data from Source shows..."

### AI-Tells to AVOID
- "In today's [X] landscape..."
- "It's important to note that..."
- "Leverage" as verb, "synergy", "best practices"
- "Furthermore", "Moreover" (excessive use)
- Starting sections with "Now let's..."

## Production Best Practices

### For Orchestrator

**When embodying an agent**:
1. Read the agent's .md file completely
2. Read all prerequisite files it requires
3. Become that agent - think and act as defined
4. Execute the workflow exactly as specified
5. Produce outputs in exact format required
6. Save to working/ directory
7. Return to orchestrator role

**Quality gate enforcement**:
- NEVER skip quality gates
- If tone-police fails (< 9.0), must address before proceeding
- If fact-checker fails (critical issues), must fix before proceeding
- Voice authenticity > convenience

**Interactive mode checkpoints**:
- Pause after each major stage
- Show preview of output
- Ask user to approve/revise/continue
- Respect user's pace

### For Voice Extraction

**Best practices**:
- Analyze 8-12 articles minimum
- Choose articles representative of target voice
- Review and edit extracted profile (especially "What to AVOID")
- Add specific examples to voice markers
- Test with a draft before full production

### Common Pitfalls to Avoid

1. **Trying to use Task tool for blog agents** - Agents are roles, not subprocesses
2. **Skipping voice profile check** - Orchestrator must verify profile exists
3. **Leading with research** - Always observation first, research validates
4. **Compromising voice for SEO** - Voice authenticity > search optimization
5. **Batch completing stages** - Complete each stage fully before next
6. **Ignoring quality gate failures** - Must address failures, cannot skip

## Working with Orchestrator

### Starting Production

```
User: "Create a blog about product-market fit challenges"

production-manager routes to:

@orchestrator start

Orchestrator handles complete workflow
```

### Commands

- `@orchestrator start` - New production
- `@orchestrator resume {slug}` - Resume in-progress
- `@orchestrator status` - Show all productions
- `@production-manager` - Entry point / general questions

## Technical Notes

### No External Dependencies for Agents
- Agent workflows use only Claude Code built-in tools
- File operations via Read/Write tools
- Web research via WebSearch/WebFetch tools
- No build process, no tests to run

### Python Voice Extractor
**Dependencies**: See `voice_extractor/requirements.txt`
- anthropic (Claude API)
- beautifulsoup4 (web scraping)
- requests (HTTP)
- python-dotenv (env vars)

**Environment**: Requires `ANTHROPIC_API_KEY` environment variable

## Key Differences from Standard Blog Writing

1. **Voice Profile Drives Everything** - Not style guides or best practices
2. **Research Supports, Never Leads** - Observation → Validation pattern
3. **Metaphors Are Structural** - Not decorative, they organize entire pieces
4. **Quality Gates Are Strict** - Must pass to publish
5. **SEO Never Compromises Voice** - Authenticity > findability
6. **Agents Are Roles** - Orchestrator embodies them, doesn't invoke via Task

## Support

For issues or questions:
- Review agent definitions in `agents/` directory
- Check README.md for user-facing documentation
- Verify voice profile exists and is complete
- Ensure ANTHROPIC_API_KEY is set for voice extraction

## Version

System: Blog Production v1.0
Claude Model: Sonnet 4.5 (claude-sonnet-4-5-20250929)
