#!/usr/bin/env python3
"""
Use LLM to detect hidden bilingual pairs by semantic comparison.
Checks if EN-only and FR-only documents are actually translations of each other.
"""

import csv
import json
import os
from openai import OpenAI
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_projects(csv_path):
    """Load projects from CSV and separate by language."""
    projects = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            projects.append(row)
    return projects

def find_existing_pairs(projects):
    """Find projects that already have bilingual pairs."""
    title_map = defaultdict(list)
    for p in projects:
        normalized = p['project_title'].lower().strip()
        title_map[normalized].append(p)
    
    paired_titles = set()
    for title, projs in title_map.items():
        langs = {p['language'] for p in projs}
        if 'en' in langs and 'fr' in langs:
            paired_titles.add(title)
    
    return paired_titles

def get_unpaired_projects(projects, paired_titles):
    """Get EN-only and FR-only projects."""
    en_only = []
    fr_only = []
    
    for p in projects:
        normalized = p['project_title'].lower().strip()
        if normalized not in paired_titles:
            if p['language'] == 'en':
                en_only.append(p)
            elif p['language'] == 'fr':
                fr_only.append(p)
    
    return en_only, fr_only

def check_semantic_match_batch(en_projects, fr_projects):
    """Use LLM to check if any EN/FR titles are translations of each other."""
    
    print(f"\n🤖 Asking GPT-4 to compare {len(en_projects)} EN titles with {len(fr_projects)} FR titles...")
    
    # Prepare data for LLM
    en_list = []
    for i, p in enumerate(en_projects, 1):
        en_list.append(f"{i}. {p['project_title']} (PDF: {p['pdf_filename']})")
    
    fr_list = []
    for i, p in enumerate(fr_projects, 1):
        fr_list.append(f"{i}. {p['project_title']} (PDF: {p['pdf_filename']})")
    
    prompt = f"""You are analyzing Canadian government AI Impact Assessment documents to find hidden bilingual pairs.

Below are two lists:
- English-only documents (no French version found by exact title matching)
- French-only documents (no English version found by exact title matching)

Your task: Identify if any English titles are semantic translations of French titles (or vice versa).

ENGLISH TITLES:
{chr(10).join(en_list)}

FRENCH TITLES:
{chr(10).join(fr_list)}

For each potential match, consider:
1. Are they about the same AI system/program?
2. Are they from the same department?
3. Do they describe the same functionality?
4. Do keywords translate between languages?

Return ONLY valid JSON array of matches. Each match should have:
- en_index: number from English list (1-based)
- fr_index: number from French list (1-based)
- confidence: "high", "medium", or "low"
- reasoning: brief explanation

If NO matches found, return empty array: []

Example format:
[
  {{
    "en_index": 3,
    "fr_index": 7,
    "confidence": "high",
    "reasoning": "Both describe passport facial recognition system for IRCC"
  }}
]

Return ONLY the JSON array, no other text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a bilingual analyst specializing in Canadian government documents. You identify semantic equivalence between English and French project titles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Extract JSON from response (in case there's extra text)
        if result_text.startswith('['):
            matches = json.loads(result_text)
        else:
            # Try to find JSON array in response
            import re
            json_match = re.search(r'\[.*\]', result_text, re.DOTALL)
            if json_match:
                matches = json.loads(json_match.group())
            else:
                print("⚠️  Could not parse LLM response as JSON")
                matches = []
        
        return matches
    
    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        return []

def main():
    print("=" * 80)
    print("🔍 DETECTING HIDDEN BILINGUAL PAIRS USING LLM")
    print("=" * 80)
    
    # Load projects
    csv_path = 'data/postgres_csvs/projects.csv'
    projects = load_projects(csv_path)
    
    print(f"\n📊 Loaded {len(projects)} total projects")
    
    # Find existing pairs
    paired_titles = find_existing_pairs(projects)
    print(f"✅ Found {len(paired_titles)} existing bilingual pairs (exact title match)")
    
    # Get unpaired projects
    en_only, fr_only = get_unpaired_projects(projects, paired_titles)
    
    print(f"\n📋 Unpaired projects:")
    print(f"  EN-only: {len(en_only)}")
    print(f"  FR-only: {len(fr_only)}")
    
    if not en_only or not fr_only:
        print("\n⚠️  Not enough unpaired projects to compare")
        return
    
    # Use LLM to find semantic matches
    matches = check_semantic_match_batch(en_only, fr_only)
    
    print(f"\n" + "=" * 80)
    print(f"🎯 SEMANTIC MATCHING RESULTS")
    print("=" * 80)
    
    if not matches:
        print("\n✓ No hidden bilingual pairs detected")
        print("  All EN-only and FR-only documents appear to be genuinely monolingual")
    else:
        print(f"\n⚠️  Found {len(matches)} potential hidden bilingual pairs!")
        print()
        
        for i, match in enumerate(matches, 1):
            en_idx = match['en_index'] - 1  # Convert to 0-based
            fr_idx = match['fr_index'] - 1
            
            en_proj = en_only[en_idx]
            fr_proj = fr_only[fr_idx]
            
            print(f"Match #{i} - Confidence: {match['confidence'].upper()}")
            print(f"  EN: {en_proj['project_title']}")
            print(f"      File: {en_proj['pdf_filename']}")
            print(f"      Dept: {en_proj['department']}")
            print()
            print(f"  FR: {fr_proj['project_title']}")
            print(f"      File: {fr_proj['pdf_filename']}")
            print(f"      Dept: {fr_proj['department']}")
            print()
            print(f"  Reasoning: {match['reasoning']}")
            print("-" * 80)
    
    # Export results
    output = {
        'summary': {
            'total_projects': len(projects),
            'existing_bilingual_pairs': len(paired_titles),
            'en_only': len(en_only),
            'fr_only': len(fr_only),
            'hidden_pairs_found': len(matches)
        },
        'en_only_projects': [
            {
                'project_id': p['project_id'],
                'title': p['project_title'],
                'filename': p['pdf_filename'],
                'department': p['department']
            } for p in en_only
        ],
        'fr_only_projects': [
            {
                'project_id': p['project_id'],
                'title': p['project_title'],
                'filename': p['pdf_filename'],
                'department': p['department']
            } for p in fr_only
        ],
        'hidden_pairs': []
    }
    
    for match in matches:
        en_idx = match['en_index'] - 1
        fr_idx = match['fr_index'] - 1
        
        output['hidden_pairs'].append({
            'en_project': {
                'project_id': en_only[en_idx]['project_id'],
                'title': en_only[en_idx]['project_title'],
                'filename': en_only[en_idx]['pdf_filename'],
                'department': en_only[en_idx]['department']
            },
            'fr_project': {
                'project_id': fr_only[fr_idx]['project_id'],
                'title': fr_only[fr_idx]['project_title'],
                'filename': fr_only[fr_idx]['pdf_filename'],
                'department': fr_only[fr_idx]['department']
            },
            'confidence': match['confidence'],
            'reasoning': match['reasoning']
        })
    
    output_file = 'research/hidden_bilingual_pairs.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Results exported to: {output_file}")
    
    # Update statistics
    print(f"\n" + "=" * 80)
    print("📊 UPDATED BILINGUAL STATISTICS")
    print("=" * 80)
    print(f"  Exact title matches:     {len(paired_titles)} pairs")
    print(f"  Hidden pairs (LLM):      {len(matches)} pairs")
    print(f"  TOTAL bilingual pairs:   {len(paired_titles) + len(matches)} pairs")
    print(f"  Truly EN-only:           {len(en_only) - len(matches)}")
    print(f"  Truly FR-only:           {len(fr_only) - len(matches)}")
    print()
    
    if matches:
        total_bilingual = len(paired_titles) + len(matches)
        bilingual_pct = (total_bilingual / len(projects)) * 100
        print(f"🎯 Bilingual availability: {bilingual_pct:.1f}% (was {(len(paired_titles)/len(projects)*100):.1f}%)")
    
    print("=" * 80)

if __name__ == '__main__':
    main()
