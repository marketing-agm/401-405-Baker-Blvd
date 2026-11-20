"""
Build the sample commercial owner report that is linked from slide 05
(Reporting) of the proposal.

The PDF is produced by AGM Report Studio itself, not mocked up by hand:

  1. Report Studio's own workbook parser (the code its Process screen runs in
     the browser) reads the Studio's FAKE commercial workbook,
     frontend/public/sample-data/sample-commercial.xlsx.
  2. We add what a property manager types on the QC screen (narrative, notes,
     projects, marketing) from scripts/sample-report/qc-notes.json.
  3. Report Studio's commercial PDF engine draws the report, exactly as the
     backend's /generate-report endpoint does in Test Mode: the
     "Report Studio Demo" signature and the diagonal SAMPLE watermark.
  4. The Studio's bundled cover page goes in front, as the Assemble step does.

No real property's numbers appear anywhere in the output.

Usage (from this repo's root, with Report Studio cloned beside it):

    python3 scripts/build-sample-report.py [path/to/report-studio]

Needs node (with `npm ci` run once in report-studio/frontend) and python with
Report Studio's pinned reportlab, pypdf and Pillow (see its
backend/requirements.txt).
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
from io import BytesIO

# Folders this script works with. The default assumes the two repos sit side by
# side, e.g. ~/code/401-405-Baker-Blvd and ~/code/report-studio.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDIO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                         else os.path.join(REPO_ROOT, '..', 'report-studio'))
NOTES_PATH = os.path.join(REPO_ROOT, 'scripts', 'sample-report', 'qc-notes.json')
OUT_PATH = os.path.join(REPO_ROOT, 'assets', 'agm-sample-commercial-owner-report.pdf')

WORKBOOK = os.path.join(STUDIO, 'frontend', 'public', 'sample-data', 'sample-commercial.xlsx')
COVER = os.path.join(STUDIO, 'frontend', 'public', 'covers', 'multifamily.pdf')  # shared MF/commercial cover
DEMO_MANAGER = 'Report Studio Demo'  # the only manager Test Mode allows

# Make Report Studio's backend modules importable (commercial_bridge etc.).
sys.path.insert(0, os.path.join(STUDIO, 'backend'))


def parse_workbook(period):
    """Run the Studio's production parser on the fake workbook and return the
    payload its Export screen would send to the backend."""
    harness = os.path.join(STUDIO, 'frontend', 'dev-parse-real-workbook.mjs')
    with tempfile.TemporaryDirectory() as tmp:
        payload_path = os.path.join(tmp, 'payload.json')
        try:
            subprocess.run(['node', harness, WORKBOOK, period, payload_path],
                           check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as err:
            sys.exit('Workbook parse failed. Did you run `npm ci` in '
                     'report-studio/frontend?\n' + err.stderr)
        with open(payload_path, encoding='utf-8') as f:
            return json.load(f)


def load_demo_manager():
    """Signature image and title for the demo manager, loaded the same way the
    backend loads them (backend/signatures/*.png and backend/pm_config.json)."""
    sig_path = os.path.join(STUDIO, 'backend', 'signatures', DEMO_MANAGER + '.png')
    with open(sig_path, 'rb') as f:
        signature = base64.b64encode(f.read()).decode('ascii')
    with open(os.path.join(STUDIO, 'backend', 'pm_config.json'), encoding='utf-8') as f:
        info = json.load(f).get(DEMO_MANAGER, {})
    return signature, info


def build_report_data(payload, notes):
    """Merge the parsed workbook with the PM's QC entries, in the shape the
    backend hands to the commercial engine (see backend/main.py)."""
    signature, pm_info = load_demo_manager()
    return {
        **payload,
        'narrative': notes['narrative'],
        'pmNotes': notes['pmNotes'],
        'priorMonth': notes['priorMonth'],
        'projectsPayload': notes['projectsPayload'],
        'marketingPayload': notes['marketingPayload'],
        'signature_png': signature,
        'pm_name': DEMO_MANAGER,
        'pm_title': pm_info.get('title', ''),
        'pm_phones': pm_info.get('phones', []),
    }


def render_report(report_data):
    """Draw the report with the Studio's commercial engine, then stamp the
    Test Mode SAMPLE watermark on every page. Returns PDF bytes."""
    import commercial_bridge
    import test_watermark
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = os.path.join(tmp, 'report.pdf')
        commercial_bridge.generate_commercial_report_from_data(report_data, pdf_path)
        with open(pdf_path, 'rb') as f:
            return test_watermark.watermark_pdf(f.read())


def add_cover(report_bytes):
    """Put the Studio's bundled cover in front of the report, as the Assemble
    step does. Returns the combined PDF bytes."""
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for page in PdfReader(COVER).pages:
        writer.add_page(page)
    for page in PdfReader(BytesIO(report_bytes)).pages:
        writer.add_page(page)
    writer.add_metadata({'/Title': 'AGM Sample Commercial Owner Report',
                         '/Author': 'AGM Real Estate Group'})
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def main():
    """Parse, merge, render, assemble and save the sample report."""
    for path in (WORKBOOK, COVER, NOTES_PATH):
        if not os.path.exists(path):
            sys.exit('Missing file: ' + path)
    with open(NOTES_PATH, encoding='utf-8') as f:
        notes = json.load(f)

    payload = parse_workbook(notes['period'])
    report = render_report(build_report_data(payload, notes))
    with open(OUT_PATH, 'wb') as f:
        f.write(add_cover(report))
    print('Wrote', os.path.relpath(OUT_PATH, REPO_ROOT))


if __name__ == '__main__':
    main()
