"""
WCAG 2.1 AA Accessibility Audit for Arrow Flasher Prototypes
Manual static analysis - no browser required
"""

import re
import json
from pathlib import Path
from html.parser import HTMLParser

class A11yChecker(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.violations = []
        self.warnings = []
        self.passes = []
        self.elements = []
        self.current_tag = None
        self.current_attrs = {}
        self.images_without_alt = []
        self.buttons_without_text = []
        self.inputs_without_labels = []
        self.links_without_text = []
        self.color_contrast_issues = []
        self.focus_issues = []
        self.aria_issues = []
        self.heading_order_issues = []
        self.landmark_issues = []
        self.table_issues = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag
        self.current_attrs = attrs_dict
        self.elements.append((tag, attrs_dict))
        
        # Check images for alt text
        if tag == 'img':
            if 'alt' not in attrs_dict:
                self.images_without_alt.append(attrs_dict.get('src', 'unknown'))
        
        # Check buttons for accessible text
        if tag == 'button':
            if not attrs_dict.get('aria-label') and not attrs_dict.get('aria-labelledby'):
                self.buttons_without_text.append(attrs_dict)
        
        # Check inputs for labels
        if tag == 'input':
            input_id = attrs_dict.get('id')
            input_type = attrs_dict.get('type', 'text')
            if input_type not in ['hidden', 'submit', 'button', 'reset']:
                if not attrs_dict.get('aria-label') and not attrs_dict.get('aria-labelledby'):
                    if not input_id:  # No ID means can't be associated with label
                        self.inputs_without_labels.append(attrs_dict)
        
        # Check links for text
        if tag == 'a':
            if not attrs_dict.get('aria-label') and not attrs_dict.get('aria-labelledby'):
                # Will check content later
                pass
        
        # Check for focus-visible styles
        if tag == 'style':
            pass  # Will check in handle_data
        
    def handle_data(self, data):
        if self.current_tag == 'style':
            # Check for :focus-visible
            if ':focus-visible' in data:
                self.passes.append('Has :focus-visible styles')
            if 'prefers-reduced-motion' in data:
                self.passes.append('Has prefers-reduced-motion media query')
            if 'prefers-contrast' in data:
                self.passes.append('Has prefers-contrast media query')

def audit_file(filepath):
    """Audit a single HTML file for WCAG 2.1 AA compliance"""
    content = filepath.read_text()
    checker = A11yChecker(filepath.name)
    
    try:
        checker.feed(content)
    except Exception as e:
        checker.violations.append(f'Parse error: {e}')
    
    # Additional checks
    # 1. Check for skip links
    if 'skip to main' in content.lower() or 'skip-link' in content.lower():
        checker.passes.append('Has skip link')
    else:
        checker.violations.append('Missing skip link (WCAG 2.4.1)')
    
    # 2. Check for main landmark
    if '<main' in content:
        checker.passes.append('Has main landmark')
    else:
        checker.warnings.append('Missing main landmark')
    
    # 3. Check for proper heading hierarchy
    headings = re.findall(r'<h([1-6])[^>]*>', content)
    if headings:
        levels = [int(h) for h in headings]
        # Check if starts with h1
        if levels[0] != 1:
            checker.warnings.append(f'First heading is h{levels[0]}, should be h1')
        # Check for skipped levels
        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                checker.warnings.append(f'Heading level skipped: h{levels[i-1]} → h{levels[i]}')
    
    # 4. Check for ARIA roles
    aria_roles = re.findall(r'role="([^"]+)"', content)
    if aria_roles:
        checker.passes.append(f'Uses ARIA roles: {", ".join(set(aria_roles))}')
    
    # 5. Check for aria-live regions
    if 'aria-live' in content:
        checker.passes.append('Has aria-live regions for dynamic content')
    
    # 6. Check for aria-expanded
    if 'aria-expanded' in content:
        checker.passes.append('Has aria-expanded for expandable elements')
    
    # 7. Check for aria-pressed
    if 'aria-pressed' in content:
        checker.passes.append('Has aria-pressed for toggle buttons')
    
    # 8. Check for aria-controls
    if 'aria-controls' in content:
        checker.passes.append('Has aria-controls for controlling elements')
    
    # 9. Check for proper form labels
    labels = re.findall(r'<label[^>]*for="([^"]+)"', content)
    inputs_with_id = re.findall(r'<input[^>]*id="([^"]+)"', content)
    if labels and inputs_with_id:
        matched = set(labels) & set(inputs_with_id)
        if matched:
            checker.passes.append(f'Form inputs have associated labels ({len(matched)} matched)')
    
    # 10. Check for color contrast (basic check)
    # Look for light text on light background or dark on dark
    if 'color: #fff' in content or 'color: white' in content:
        # Check if background is also light
        if 'background: #fff' in content or 'background: white' in content:
            checker.warnings.append('Potential color contrast issue: white text on white background')
    
    # 11. Check for responsive design
    if 'viewport' in content and 'width=device-width' in content:
        checker.passes.append('Has viewport meta tag for responsive design')
    else:
        checker.warnings.append('Missing viewport meta tag')
    
    # 12. Check for lang attribute
    if '<html lang=' in content:
        checker.passes.append('Has lang attribute on html element')
    else:
        checker.violations.append('Missing lang attribute on html element (WCAG 3.1.1)')
    
    # 13. Check for title
    if '<title>' in content:
        checker.passes.append('Has page title')
    else:
        checker.violations.append('Missing page title (WCAG 2.4.2)')
    
    # 14. Check for tables with headers
    tables = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL)
    for table in tables:
        if '<th' in table:
            checker.passes.append('Table has header cells')
        else:
            checker.warnings.append('Table missing header cells')
    
    return {
        'file': filepath.name,
        'violations': checker.violations,
        'warnings': checker.warnings,
        'passes': checker.passes,
        'violation_count': len(checker.violations),
        'warning_count': len(checker.warnings),
        'pass_count': len(checker.passes)
    }

def main():
    worktree = Path('/home/roma/worktrees/arrow-flasher-prototypes-p1')
    html_files = sorted(worktree.glob('*.html'))
    
    results = []
    for html_file in html_files:
        print(f'Auditing {html_file.name}...')
        result = audit_file(html_file)
        results.append(result)
        print(f'  ✓ {result["pass_count"]} passes, ⚠ {result["warning_count"]} warnings, ✗ {result["violation_count"]} violations')
    
    # Generate report
    report = {
        'timestamp': '2026-08-27T06:40:00Z',
        'tool': 'Manual WCAG 2.1 AA Static Analysis',
        'total_files': len(results),
        'summary': {
            'total_violations': sum(r['violation_count'] for r in results),
            'total_warnings': sum(r['warning_count'] for r in results),
            'total_passes': sum(r['pass_count'] for r in results)
        },
        'results': results
    }
    
    report_path = worktree / 'a11y-report.json'
    report_path.write_text(json.dumps(report, indent=2))
    
    print(f'\n=== Summary ===')
    print(f'Total violations: {report["summary"]["total_violations"]}')
    print(f'Total warnings: {report["summary"]["total_warnings"]}')
    print(f'Total passes: {report["summary"]["total_passes"]}')
    print(f'\nFull report saved to {report_path.name}')

if __name__ == '__main__':
    main()
