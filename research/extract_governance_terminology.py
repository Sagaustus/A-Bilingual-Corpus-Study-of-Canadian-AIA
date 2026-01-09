#!/usr/bin/env python3
"""
Extract and compare governance terminology from 18 bilingual pairs.
Focus: translation, meaning, semantic drift in governance concepts.
"""

import json
import os
import re
from collections import defaultdict, Counter
from pathlib import Path
from pdfminer.high_level import extract_text
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Key governance terms to track
GOVERNANCE_TERMS_EN = [
    'oversight', 'supervision', 'monitoring', 'surveillance',
    'accountability', 'responsibility', 'liable', 'accountable',
    'transparency', 'openness', 'disclosure',
    'fairness', 'equity', 'justice', 'bias', 'discrimination',
    'appeal', 'recourse', 'review', 'challenge',
    'human review', 'human oversight', 'human judgment', 'human intervention',
    'audit', 'evaluation', 'assessment',
    'explanation', 'interpretability', 'explainability'
]

GOVERNANCE_TERMS_FR = [
    'surveillance', 'supervision', 'contrôle', 'suivi',
    'responsabilité', 'imputabilité', 'redevabilité',
    'transparence', 'ouverture', 'divulgation',
    'équité', 'justice', 'biais', 'discrimination', 'préjugé',
    'recours', 'appel', 'révision', 'contestation',
    'examen humain', 'surveillance humaine', 'jugement humain', 'intervention humaine',
    'audit', 'évaluation', 'vérification',
    'explication', 'interprétabilité', 'explicabilité'
]

def load_bilingual_pairs():
    """Load the 18 bilingual pairs from JSON."""
    pairs_file = 'research/hidden_bilingual_pairs.json'
    with open(pairs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Combine existing pairs and hidden pairs
    all_pairs = data['hidden_pairs']
    
    print(f"✅ Loaded {len(all_pairs)} bilingual pairs")
    return all_pairs

def extract_pdf_text(pdf_path):
    """Extract text from PDF file."""
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"  ⚠️  Error extracting {pdf_path}: {e}")
        return ""

def find_term_contexts(text, term, window=50):
    """Find all occurrences of a term with surrounding context."""
    contexts = []
    text_lower = text.lower()
    term_lower = term.lower()
    
    # Find all positions
    pos = 0
    while True:
        pos = text_lower.find(term_lower, pos)
        if pos == -1:
            break
        
        # Extract context window
        start = max(0, pos - window)
        end = min(len(text), pos + len(term) + window)
        context = text[start:end].strip()
        
        contexts.append({
            'term': term,
            'position': pos,
            'context': context
        })
        
        pos += len(term)
    
    return contexts

def extract_governance_terms_from_text(text, terms, language):
    """Extract governance terms and their contexts from text."""
    results = {
        'term_frequencies': Counter(),
        'term_contexts': defaultdict(list)
    }
    
    for term in terms:
        contexts = find_term_contexts(text, term)
        if contexts:
            results['term_frequencies'][term] = len(contexts)
            results['term_contexts'][term] = contexts[:3]  # Keep first 3 examples
    
    return results

def analyze_semantic_drift_with_llm(en_text, fr_text, en_proj, fr_proj):
    """Use LLM to identify semantic drift in governance terminology."""
    
    print(f"  🤖 Analyzing semantic drift for: {en_proj['title'][:50]}...")
    
    # Truncate texts to manageable size
    en_sample = en_text[:3000]
    fr_sample = fr_text[:3000]
    
    prompt = f"""You are a bilingual translation analyst specializing in governance terminology.

Compare these two AI Impact Assessment documents (English and French versions of the same project):

PROJECT: {en_proj['title']}

ENGLISH EXCERPT:
{en_sample}

FRENCH EXCERPT:
{fr_sample}

Analyze:
1. Key governance terms used in each language
2. Semantic differences in how accountability, oversight, transparency are described
3. Terms present in one language but absent/different in the other
4. Connotational differences (e.g., "oversight" vs "surveillance")

Return JSON with:
{{
  "key_terms_en": [list of important governance terms in English],
  "key_terms_fr": [list of important governance terms in French],
  "semantic_differences": [
    {{
      "en_term": "term in English",
      "fr_term": "corresponding term in French",
      "difference": "explanation of semantic drift"
    }}
  ],
  "omissions_en": [concepts present in FR but not EN],
  "omissions_fr": [concepts present in EN but not FR],
  "overall_assessment": "brief summary of translation quality and semantic alignment"
}}

Return ONLY valid JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a translation studies expert analyzing semantic drift in bilingual government documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Extract JSON
        if result_text.startswith('{'):
            analysis = json.loads(result_text)
        else:
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                analysis = {"error": "Could not parse LLM response"}
        
        return analysis
    
    except Exception as e:
        print(f"    ❌ LLM error: {e}")
        return {"error": str(e)}

def main():
    print("=" * 80)
    print("📚 GOVERNANCE TERMINOLOGY EXTRACTION")
    print("=" * 80)
    
    # Load bilingual pairs
    pairs = load_bilingual_pairs()
    
    # Prepare output directory
    output_dir = Path('research/governance_terminology')
    output_dir.mkdir(exist_ok=True)
    
    # Results storage
    all_results = {
        'summary': {
            'total_pairs': len(pairs),
            'en_term_totals': Counter(),
            'fr_term_totals': Counter()
        },
        'pair_analyses': []
    }
    
    print(f"\n📄 Processing {len(pairs)} bilingual pairs...\n")
    
    for i, pair in enumerate(pairs, 1):
        print(f"[{i}/{len(pairs)}] {pair['en_project']['title'][:60]}...")
        
        # Build PDF paths
        en_pdf = Path('data/pdfs/en') / pair['en_project']['filename']
        fr_pdf = Path('data/pdfs/fr') / pair['fr_project']['filename']
        
        # Extract text
        en_text = extract_pdf_text(en_pdf)
        fr_text = extract_pdf_text(fr_pdf)
        
        if not en_text or not fr_text:
            print(f"  ⚠️  Skipping - could not extract text")
            continue
        
        # Extract governance terms
        en_analysis = extract_governance_terms_from_text(en_text, GOVERNANCE_TERMS_EN, 'en')
        fr_analysis = extract_governance_terms_from_text(fr_text, GOVERNANCE_TERMS_FR, 'fr')
        
        # Update totals
        all_results['summary']['en_term_totals'].update(en_analysis['term_frequencies'])
        all_results['summary']['fr_term_totals'].update(fr_analysis['term_frequencies'])
        
        # LLM semantic analysis
        llm_analysis = analyze_semantic_drift_with_llm(en_text, fr_text, pair['en_project'], pair['fr_project'])
        
        # Store results for this pair
        pair_result = {
            'pair_number': i,
            'en_project': {
                'id': pair['en_project']['project_id'],
                'title': pair['en_project']['title'],
                'filename': pair['en_project']['filename'],
                'department': pair['en_project']['department']
            },
            'fr_project': {
                'id': pair['fr_project']['project_id'],
                'title': pair['fr_project']['title'],
                'filename': pair['fr_project']['filename'],
                'department': pair['fr_project']['department']
            },
            'term_analysis': {
                'en_frequencies': dict(en_analysis['term_frequencies']),
                'fr_frequencies': dict(fr_analysis['term_frequencies']),
                'en_total_terms': sum(en_analysis['term_frequencies'].values()),
                'fr_total_terms': sum(fr_analysis['term_frequencies'].values())
            },
            'llm_semantic_analysis': llm_analysis,
            'sample_contexts': {
                'en': {term: contexts for term, contexts in list(en_analysis['term_contexts'].items())[:5]},
                'fr': {term: contexts for term, contexts in list(fr_analysis['term_contexts'].items())[:5]}
            }
        }
        
        all_results['pair_analyses'].append(pair_result)
        
        print(f"  ✅ EN: {sum(en_analysis['term_frequencies'].values())} governance terms found")
        print(f"  ✅ FR: {sum(fr_analysis['term_frequencies'].values())} governance terms found")
    
    # Generate summary statistics
    print(f"\n" + "=" * 80)
    print("📊 SUMMARY STATISTICS")
    print("=" * 80)
    
    print("\n🔤 TOP GOVERNANCE TERMS (ENGLISH):")
    for term, count in all_results['summary']['en_term_totals'].most_common(15):
        print(f"  {term:25} → {count:3} occurrences")
    
    print("\n🔤 TOP GOVERNANCE TERMS (FRENCH):")
    for term, count in all_results['summary']['fr_term_totals'].most_common(15):
        print(f"  {term:25} → {count:3} occurrences")
    
    # Export full results
    output_file = output_dir / 'full_terminology_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Full results exported to: {output_file}")
    
    # Create comparative terminology table
    create_comparative_table(all_results, output_dir)
    
    # Create semantic drift report
    create_semantic_drift_report(all_results, output_dir)
    
    print("=" * 80)

def create_comparative_table(results, output_dir):
    """Create CSV comparing EN/FR terminology usage."""
    import csv
    
    output_file = output_dir / 'en_fr_terminology_comparison.csv'
    
    # Get all unique terms
    en_totals = results['summary']['en_term_totals']
    fr_totals = results['summary']['fr_term_totals']
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'EN Term', 'EN Count', 'FR Term', 'FR Count', 'Ratio (EN/FR)'])
        
        # Accountability terms
        writer.writerow(['Accountability', 'accountability', en_totals.get('accountability', 0), 
                        'responsabilité', fr_totals.get('responsabilité', 0),
                        f"{en_totals.get('accountability', 0) / max(fr_totals.get('responsabilité', 1), 1):.2f}"])
        
        # Oversight terms
        writer.writerow(['Oversight', 'oversight', en_totals.get('oversight', 0),
                        'surveillance', fr_totals.get('surveillance', 0),
                        f"{en_totals.get('oversight', 0) / max(fr_totals.get('surveillance', 1), 1):.2f}"])
        
        # Transparency
        writer.writerow(['Transparency', 'transparency', en_totals.get('transparency', 0),
                        'transparence', fr_totals.get('transparence', 0),
                        f"{en_totals.get('transparency', 0) / max(fr_totals.get('transparence', 1), 1):.2f}"])
        
        # Fairness/Equity
        writer.writerow(['Fairness', 'fairness', en_totals.get('fairness', 0),
                        'équité', fr_totals.get('équité', 0),
                        f"{en_totals.get('fairness', 0) / max(fr_totals.get('équité', 1), 1):.2f}"])
        
        writer.writerow(['Equity', 'equity', en_totals.get('equity', 0),
                        'équité', fr_totals.get('équité', 0),
                        f"{en_totals.get('equity', 0) / max(fr_totals.get('équité', 1), 1):.2f}"])
        
        # Human review
        writer.writerow(['Human Review', 'human review', en_totals.get('human review', 0),
                        'examen humain', fr_totals.get('examen humain', 0),
                        f"{en_totals.get('human review', 0) / max(fr_totals.get('examen humain', 1), 1):.2f}"])
    
    print(f"  📊 Comparative table: {output_file}")

def create_semantic_drift_report(results, output_dir):
    """Create markdown report of semantic drift findings."""
    
    output_file = output_dir / 'semantic_drift_report.md'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Semantic Drift in Bilingual AI Governance Documents\n\n")
        f.write(f"**Analysis Date:** January 9, 2026\n")
        f.write(f"**Documents Analyzed:** {results['summary']['total_pairs']} bilingual pairs\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This report documents semantic drift between English and French versions ")
        f.write("of Canadian AI Impact Assessments.\n\n")
        
        f.write("## Key Findings by Project\n\n")
        
        for pair in results['pair_analyses']:
            if 'llm_semantic_analysis' in pair and 'error' not in pair['llm_semantic_analysis']:
                analysis = pair['llm_semantic_analysis']
                
                f.write(f"### {pair['pair_number']}. {pair['en_project']['title']}\n\n")
                f.write(f"**Department:** {pair['en_project']['department']}\n\n")
                
                if 'semantic_differences' in analysis and analysis['semantic_differences']:
                    f.write("**Semantic Differences:**\n\n")
                    for diff in analysis['semantic_differences']:
                        f.write(f"- **EN:** `{diff.get('en_term', 'N/A')}` → ")
                        f.write(f"**FR:** `{diff.get('fr_term', 'N/A')}`\n")
                        f.write(f"  - {diff.get('difference', 'No explanation provided')}\n\n")
                
                if 'overall_assessment' in analysis:
                    f.write(f"**Assessment:** {analysis['overall_assessment']}\n\n")
                
                f.write("---\n\n")
    
    print(f"  📄 Semantic drift report: {output_file}")

if __name__ == '__main__':
    main()
