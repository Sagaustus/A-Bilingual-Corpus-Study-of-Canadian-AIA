#!/usr/bin/env python3
"""
AIA PDF Downloader - Bilingual Corpus Builder

Downloads all PDF files from Open Canada AIA dataset pages.
Organizes into EN/FR folders with mapping for bilingual analysis.

Usage:
    python research/download_pdfs.py --csv "Algorithmic Impact Assessment Links - Sheet1 (1).csv"
    python research/download_pdfs.py --dry-run  # test without downloading
"""

import argparse
import csv
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class BilingualPDFDownloader:
    """Downloads and organizes bilingual AIA PDFs."""
    
    def __init__(self, output_dir="data/pdfs", dry_run=False):
        self.output_dir = Path(output_dir)
        self.en_dir = self.output_dir / "en"
        self.fr_dir = self.output_dir / "fr"
        self.dry_run = dry_run
        
        # Create directories
        if not dry_run:
            self.en_dir.mkdir(parents=True, exist_ok=True)
            self.fr_dir.mkdir(parents=True, exist_ok=True)
        
        self.mapping = []  # List of {en_path, fr_path, title, url}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AIA-Research-Bot/1.0; +https://github.com/canada-ca/aia-eia-js)'
        })
    
    def detect_language(self, url, text):
        """Detect if PDF link is English or French."""
        url_lower = url.lower()
        text_lower = text.lower()
        
        # Strong URL patterns (most reliable)
        if '-en.pdf' in url_lower or '-eng.pdf' in url_lower or '_en.pdf' in url_lower or '_eng.pdf' in url_lower:
            return 'en'
        if '-fr.pdf' in url_lower or '-fra.pdf' in url_lower or '_fr.pdf' in url_lower or '_fra.pdf' in url_lower:
            return 'fr'
        
        # URL path patterns
        if '/eng/' in url_lower or '/en/' in url_lower or '/english/' in url_lower:
            return 'en'
        if '/fra/' in url_lower or '/fr/' in url_lower or '/french/' in url_lower or '/francais/' in url_lower:
            return 'fr'
        
        # French-specific keywords in URL (strong indicators)
        french_keywords = ['resultats', 'résultats', 'evaluation', 'évaluation', 'algorithmique',
                          'analyse', 'sexes', 'pour-le', 'du-', 'de-l', 'des-']
        if any(kw in url_lower for kw in french_keywords):
            return 'fr'
        
        # English-specific keywords in URL
        english_keywords = ['summary-for', 'annex-a', 'assessment-', 'system-', 'recognition-system']
        if any(kw in url_lower for kw in english_keywords):
            return 'en'
        
        # Filename word patterns
        if 'english' in url_lower or '-anglais' in url_lower:
            return 'en'
        if 'french' in url_lower or 'francais' in url_lower or 'français' in url_lower:
            return 'fr'
        
        # Text patterns (anchor text or nearby context)
        # Explicit language indicators
        if '(english)' in text_lower or '(anglais)' in text_lower:
            return 'en'
        if '(french)' in text_lower or '(français)' in text_lower or '(francais)' in text_lower:
            return 'fr'
        
        # Common document titles
        if 'english' in text_lower:
            return 'en'
        if 'french' in text_lower or 'francais' in text_lower or 'français' in text_lower:
            return 'fr'
        
        # If we can't detect, return None (will need manual review)
        return None
    
    def sanitize_filename(self, title):
        """Create clean filename from title."""
        # Remove special chars, limit length
        clean = re.sub(r'[^\w\s-]', '', title)
        clean = re.sub(r'\s+', '_', clean)
        return clean[:100]  # Max 100 chars
    
    def find_pdf_links(self, url):
        """Find all PDF download links on an Open Canada dataset page."""
        try:
            print(f"\n📄 Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Open Canada uses specific structure for dataset resources
            pdf_links = []
            
            # Method 1: Find all PDF links in resource list
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Check if it's a PDF
                if href.lower().endswith('.pdf') or 'format=pdf' in href.lower():
                    # Get context (link text + parent text)
                    link_text = link.get_text(strip=True)
                    parent_text = link.parent.get_text(strip=True) if link.parent else ''
                    context = f"{link_text} {parent_text}"
                    
                    # Resolve relative URLs
                    full_url = urljoin(url, href)
                    
                    # Detect language
                    lang = self.detect_language(full_url, context)
                    
                    pdf_links.append({
                        'url': full_url,
                        'text': link_text,
                        'context': context,
                        'lang': lang
                    })
            
            # Method 2: Check for downloadable resources section
            resource_section = soup.find('section', {'class': 'resources'}) or \
                             soup.find('div', {'class': 'resource-list'})
            
            if resource_section:
                for link in resource_section.find_all('a', href=True):
                    href = link['href']
                    if href.lower().endswith('.pdf'):
                        full_url = urljoin(url, href)
                        # Avoid duplicates
                        if not any(p['url'] == full_url for p in pdf_links):
                            link_text = link.get_text(strip=True)
                            lang = self.detect_language(full_url, link_text)
                            pdf_links.append({
                                'url': full_url,
                                'text': link_text,
                                'context': link_text,
                                'lang': lang
                            })
            
            print(f"  ✓ Found {len(pdf_links)} PDF link(s)")
            return pdf_links
        
        except Exception as e:
            print(f"  ✗ Error fetching {url}: {e}")
            return []
    
    def download_pdf(self, pdf_url, output_path):
        """Download a single PDF file."""
        try:
            if self.dry_run:
                print(f"  [DRY-RUN] Would download to: {output_path}")
                return True
            
            response = self.session.get(pdf_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Verify it's actually a PDF
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' not in content_type.lower():
                print(f"  ⚠️  Warning: Content-Type is {content_type}, not PDF")
            
            # Write to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ Downloaded: {output_path.name}")
            return True
        
        except Exception as e:
            print(f"  ✗ Error downloading {pdf_url}: {e}")
            return False
    
    def process_dataset(self, title, url):
        """Process a single AIA dataset page."""
        print(f"\n{'='*80}")
        print(f"Dataset: {title}")
        
        # Find all PDFs on the page
        pdf_links = self.find_pdf_links(url)
        
        if not pdf_links:
            print("  ⚠️  No PDFs found")
            return
        
        # Group by language
        en_pdfs = [p for p in pdf_links if p['lang'] == 'en']
        fr_pdfs = [p for p in pdf_links if p['lang'] == 'fr']
        unknown_pdfs = [p for p in pdf_links if p['lang'] is None]
        
        print(f"\n  Languages detected:")
        print(f"    EN: {len(en_pdfs)}")
        print(f"    FR: {len(fr_pdfs)}")
        if unknown_pdfs:
            print(f"    Unknown: {len(unknown_pdfs)} (needs manual review)")
        
        # Create base filename from dataset title
        base_filename = self.sanitize_filename(title)
        
        # Download English PDFs
        en_paths = []
        for i, pdf in enumerate(en_pdfs):
            filename = f"{base_filename}_en_{i+1}.pdf" if len(en_pdfs) > 1 else f"{base_filename}_en.pdf"
            output_path = self.en_dir / filename
            
            if self.download_pdf(pdf['url'], output_path):
                en_paths.append(str(output_path.relative_to(self.output_dir)))
        
        # Download French PDFs
        fr_paths = []
        for i, pdf in enumerate(fr_pdfs):
            filename = f"{base_filename}_fr_{i+1}.pdf" if len(fr_pdfs) > 1 else f"{base_filename}_fr.pdf"
            output_path = self.fr_dir / filename
            
            if self.download_pdf(pdf['url'], output_path):
                fr_paths.append(str(output_path.relative_to(self.output_dir)))
        
        # Download unknown (flag for manual review)
        for i, pdf in enumerate(unknown_pdfs):
            filename = f"{base_filename}_UNKNOWN_{i+1}.pdf"
            output_path = self.output_dir / "unknown" / filename
            
            if not self.dry_run:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"\n  ⚠️  Manual review needed: {pdf['url']}")
            print(f"     Context: {pdf['context'][:100]}")
            
            if self.download_pdf(pdf['url'], output_path):
                print(f"     Saved to: {output_path.relative_to(self.output_dir)}")
        
        # Create mapping entry
        if en_paths or fr_paths:
            self.mapping.append({
                'title': title,
                'url': url,
                'en_files': en_paths,
                'fr_files': fr_paths,
                'has_both': bool(en_paths and fr_paths)
            })
        
        # Rate limiting (be nice to servers)
        time.sleep(2)
    
    def load_csv(self, csv_path):
        """Load dataset URLs from CSV."""
        datasets = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Algorithmic Impact Assessment', '').strip()
                url = row.get('Link', '').strip()
                if title and url:
                    datasets.append({'title': title, 'url': url})
        return datasets
    
    def save_mapping(self):
        """Save bilingual mapping to JSON."""
        if self.dry_run:
            print("\n[DRY-RUN] Would save mapping to: data/pdfs/bilingual_mapping.json")
            return
        
        mapping_path = self.output_dir / "bilingual_mapping.json"
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_datasets': len(self.mapping),
                'bilingual_count': sum(1 for m in self.mapping if m['has_both']),
                'en_only_count': sum(1 for m in self.mapping if m['en_files'] and not m['fr_files']),
                'fr_only_count': sum(1 for m in self.mapping if m['fr_files'] and not m['en_files']),
                'datasets': self.mapping
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Mapping saved to: {mapping_path}")
    
    def print_summary(self):
        """Print summary statistics."""
        print(f"\n{'='*80}")
        print("📊 DOWNLOAD SUMMARY")
        print(f"{'='*80}")
        
        total = len(self.mapping)
        bilingual = sum(1 for m in self.mapping if m['has_both'])
        en_only = sum(1 for m in self.mapping if m['en_files'] and not m['fr_files'])
        fr_only = sum(1 for m in self.mapping if m['fr_files'] and not m['en_files'])
        
        print(f"Total datasets processed: {total}")
        print(f"  ✓ Bilingual (EN + FR): {bilingual}")
        print(f"  ⚠️  EN only: {en_only}")
        print(f"  ⚠️  FR only: {fr_only}")
        
        total_en = sum(len(m['en_files']) for m in self.mapping)
        total_fr = sum(len(m['fr_files']) for m in self.mapping)
        
        print(f"\nTotal PDF files:")
        print(f"  EN: {total_en}")
        print(f"  FR: {total_fr}")
        
        if bilingual < total:
            print(f"\n⚠️  {total - bilingual} dataset(s) missing bilingual pair(s)")
            print("   Check unknown/ folder or page for additional resources")


def main():
    parser = argparse.ArgumentParser(description="Download bilingual AIA PDFs")
    parser.add_argument(
        '--csv',
        default='Algorithmic Impact Assessment Links - Sheet1 (1).csv',
        help='Path to CSV file with dataset URLs'
    )
    parser.add_argument(
        '--output',
        default='data/pdfs',
        help='Output directory for downloaded PDFs'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test without downloading files'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of datasets to process (for testing)'
    )
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = BilingualPDFDownloader(
        output_dir=args.output,
        dry_run=args.dry_run
    )
    
    # Load datasets from CSV
    print(f"📂 Loading datasets from: {args.csv}")
    datasets = downloader.load_csv(args.csv)
    print(f"   Found {len(datasets)} dataset(s)")
    
    if args.limit:
        datasets = datasets[:args.limit]
        print(f"   Limited to first {args.limit} dataset(s)")
    
    # Process each dataset
    for dataset in datasets:
        downloader.process_dataset(dataset['title'], dataset['url'])
    
    # Save mapping
    downloader.save_mapping()
    
    # Print summary
    downloader.print_summary()
    
    print(f"\n{'='*80}")
    print("✅ DONE")
    print(f"{'='*80}")
    
    if not args.dry_run:
        print(f"\nNext steps:")
        print(f"  1. Check unknown/ folder for files needing language classification")
        print(f"  2. Review bilingual_mapping.json for paired documents")
        print(f"  3. Run text extraction: python research/extract_text.py")


if __name__ == "__main__":
    main()
