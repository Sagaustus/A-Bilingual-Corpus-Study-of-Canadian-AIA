#!/usr/bin/env python3
"""
Bilingual Conceptual Divergence Analysis using LLMs

Analyzes English-French AIA pairs to identify "untranslatable" governance concepts
using semantic similarity, conceptual mapping, and terminological divergence detection.

This script does NOT translate; it analyzes where direct equivalence breaks down.
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
import re

import dotenv
from openai import OpenAI

# Load environment
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 2000))
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.3))

# AI Ethics terminology to analyze
KEY_TERMS = {
    "fairness": ["bias", "equity", "discrimination", "justice"],
    "transparency": ["explainability", "interpretability", "accountability"],
    "governance": ["oversight", "audit", "human review", "control"],
    "privacy": ["data protection", "PII", "consent", "anonymization"],
}

ANALYSIS_PROMPT = """
You are a Digital Humanities researcher analyzing bilingual policy documents.

Task: Compare how AI ethics and governance concepts are expressed differently in English vs. French Algorithmic Impact Assessments.

English passage:
---
{en_text}
---

French passage (addressing the same topic):
---
{fr_text}
---

Analyze the following:

1. **Term Mapping**: Identify key terms in each language. Are there direct equivalents?
2. **Conceptual Divergence**: Where do the English and French terms diverge in meaning or emphasis?
3. **Philosophical Assumptions**: What different assumptions about AI governance, human agency, or responsibility do these terms encode?
4. **Untranslatability**: Which concepts resist direct translation and why?
5. **Terminological Category**: Is this divergence due to:
   - Linguistic structure (EN vs FR grammar/syntax)?
   - Legal/administrative tradition (Common Law vs Civil Law)?
   - Cultural values (individualism vs collectivism)?
   - Professional jargon (tech vs public admin)?

Format your response as JSON:
{
  "en_key_terms": ["term1", "term2"],
  "fr_key_terms": ["terme1", "terme2"],
  "direct_equivalents": {"term": "equivalent"} or {},
  "divergence_analysis": "explanation",
  "philosophical_assumptions": {
    "english": "assumption1",
    "french": "assumption2"
  },
  "untranslatable_concepts": ["concept1", "concept2"],
  "divergence_origin": "linguistic|legal|cultural|professional",
  "confidence": 0.0-1.0
}
"""

def load_bilingual_pairs(data_dir="data/processed"):
    """Load processed records with EN/FR text extracts."""
    pairs = []
    processed_path = Path(data_dir)
    
    if not processed_path.exists():
        print(f"⚠ No processed data found at {data_dir}")
        print("Run: python research/crawl.py && python research/extract_text.py && python research/normalize.py")
        return []
    
    for record_dir in processed_path.iterdir():
        if not record_dir.is_dir():
            continue
        
        normalized_file = record_dir / "normalized.json"
        if normalized_file.exists():
            with open(normalized_file) as f:
                record = json.load(f)
            
            # Extract EN and FR snippets
            en_snippet = record.get("snippets", {}).get("en", "")
            fr_snippet = record.get("snippets", {}).get("fr", "")
            
            if en_snippet and fr_snippet:
                pairs.append({
                    "record_id": record_dir.name,
                    "title": record.get("title", ""),
                    "en_text": en_snippet,
                    "fr_text": fr_snippet,
                    "tags": record.get("tags", [])
                })
    
    return pairs

def analyze_pair(pair, output_file=None):
    """Send bilingual pair to LLM for conceptual divergence analysis."""
    prompt = ANALYSIS_PROMPT.format(
        en_text=pair["en_text"][:1000],  # Limit to first 1000 chars
        fr_text=pair["fr_text"][:1000]
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a DH researcher analyzing bilingual policy documents. Respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        analysis_text = response.choices[0].message.content.strip()
        
        # Extract JSON (LLM might wrap it in markdown)
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            analysis = json.loads(analysis_text)
        
        analysis["record_id"] = pair["record_id"]
        analysis["title"] = pair["title"]
        analysis["usage"] = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        }
        
        if output_file:
            with open(output_file, "a") as f:
                f.write(json.dumps(analysis) + "\n")
        
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error for {pair['record_id']}: {e}")
        return None
    except Exception as e:
        print(f"✗ API error for {pair['record_id']}: {e}")
        return None

def aggregate_divergences(analyses):
    """Aggregate divergence patterns across all pairs."""
    stats = {
        "total_pairs": len(analyses),
        "linguistic_divergences": 0,
        "legal_divergences": 0,
        "cultural_divergences": 0,
        "professional_divergences": 0,
        "untranslatable_terms": defaultdict(int),
        "avg_confidence": 0.0,
        "divergence_examples": []
    }
    
    confidences = []
    
    for analysis in analyses:
        if not analysis:
            continue
        
        origin = analysis.get("divergence_origin", "").lower()
        if origin == "linguistic":
            stats["linguistic_divergences"] += 1
        elif origin == "legal":
            stats["legal_divergences"] += 1
        elif origin == "cultural":
            stats["cultural_divergences"] += 1
        elif origin == "professional":
            stats["professional_divergences"] += 1
        
        # Count untranslatable concepts
        for concept in analysis.get("untranslatable_concepts", []):
            stats["untranslatable_terms"][concept] += 1
        
        # Track confidence
        if "confidence" in analysis:
            confidences.append(analysis["confidence"])
        
        # Store example divergences
        if analysis.get("divergence_analysis"):
            stats["divergence_examples"].append({
                "record": analysis.get("record_id"),
                "analysis": analysis.get("divergence_analysis")[:200]
            })
    
    if confidences:
        stats["avg_confidence"] = sum(confidences) / len(confidences)
    
    # Sort untranslatable terms by frequency
    stats["untranslatable_terms"] = dict(
        sorted(stats["untranslatable_terms"].items(), 
               key=lambda x: x[1], reverse=True)
    )
    
    return stats

def generate_report(stats, output_file="research/output/divergence_report.json"):
    """Generate final divergence report."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("BILINGUAL CONCEPTUAL DIVERGENCE ANALYSIS")
    print("="*70)
    print(f"\nAnalyzed {stats['total_pairs']} EN/FR AIA pairs\n")
    
    print("Divergence Origins:")
    print(f"  Linguistic: {stats['linguistic_divergences']} ({stats['linguistic_divergences']/max(stats['total_pairs'],1)*100:.1f}%)")
    print(f"  Legal/Administrative: {stats['legal_divergences']} ({stats['legal_divergences']/max(stats['total_pairs'],1)*100:.1f}%)")
    print(f"  Cultural: {stats['cultural_divergences']} ({stats['cultural_divergences']/max(stats['total_pairs'],1)*100:.1f}%)")
    print(f"  Professional: {stats['professional_divergences']} ({stats['professional_divergences']/max(stats['total_pairs'],1)*100:.1f}%)")
    print(f"  Average Confidence: {stats['avg_confidence']:.2f}\n")
    
    print(f"Top Untranslatable Concepts:")
    for term, count in list(stats["untranslatable_terms"].items())[:10]:
        print(f"  • {term}: {count} occurrences")
    
    print(f"\nFull report saved to: {output_file}\n")

def main():
    """Main analysis pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze bilingual conceptual divergence in AIAs")
    parser.add_argument("--limit", type=int, default=None, help="Limit to N pairs (for testing)")
    parser.add_argument("--output", default="research/output/divergence_analyses.jsonl", 
                        help="Output file for analyses")
    parser.add_argument("--dry-run", action="store_true", help="Show pairs without calling API")
    
    args = parser.parse_args()
    
    # Load pairs
    print("Loading bilingual AIA pairs...")
    pairs = load_bilingual_pairs()
    
    if not pairs:
        print("No bilingual pairs found. Ensure corpus is processed first.")
        sys.exit(1)
    
    if args.limit:
        pairs = pairs[:args.limit]
    
    print(f"Found {len(pairs)} bilingual pairs\n")
    
    # Analyze each pair
    if args.dry_run:
        print("Dry run mode: showing sample pairs\n")
        for pair in pairs[:2]:
            print(f"Record: {pair['title']}")
            print(f"  EN: {pair['en_text'][:100]}...")
            print(f"  FR: {pair['fr_text'][:100]}...\n")
        return
    
    # Clear output file
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        pass
    
    analyses = []
    for i, pair in enumerate(pairs, 1):
        print(f"[{i}/{len(pairs)}] Analyzing {pair['record_id']}...", end=" ")
        analysis = analyze_pair(pair, output_file=args.output)
        
        if analysis:
            analyses.append(analysis)
            print(f"✓ Confidence: {analysis.get('confidence', 'N/A')}")
        else:
            print("✗ Failed")
    
    # Aggregate and report
    if analyses:
        stats = aggregate_divergences(analyses)
        generate_report(stats)
    else:
        print("No analyses completed.")

if __name__ == "__main__":
    main()
