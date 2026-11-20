# AGM Real Estate Group: 401 & 405 Baker Blvd Proposal Micro-Site

**CONFIDENTIAL: proposal material. Private repository. Do not make public.**

A digital proposal for Management Services at 401 and 405 Baker Blvd, Tukwila, WA 98188, prepared for
401 Baker LLC and 405 Baker LLC. It is a single-file static site (`index.html`, no build step, no
dependencies). Fonts load from Google Fonts; everything else is inline.

The site is a copy of the 838 Seneca Ave SW proposal (`marketing-agm/commercial-seneca-ave-sw`, `main`
as of 2026-11-20), with the same design system, structure, navigation, print stylesheet, PDF build and
analytics, and with the copy rewritten for these two buildings.

## What this is
A single Cover page (letter, aerial plate and contents), then nine sections:

1. The Property · 2. Your Team · 3. The First 90 Days · 4. Day-to-Day Management · 5. Reporting &
the Owner Portal · 6. Investment Strategy · 7. Track Record · 8. Management Fees · 9. Agreement &
Contact.

### How it differs from the Seneca proposal
Seneca was one vacant, single-tenant building with another broker marketing it. Baker Blvd is two
leased buildings held by two LLCs, whose owners are leaving a long-time manager who was a family
friend and who have not been involved in day-to-day operations. The copy follows from that:

- **Two entities.** The King County record confirms 401 Baker LLC (parcel 022310-0085) and 405 Baker
  LLC (parcel 022310-0087) are separate. The proposal sets one agreement, separate bank accounts and
  separate books per entity, with one combined Owner Portal view. See "Two Entities" on slide 01.
- **Transparency, tools and reporting** lead the cover letter, the Day-to-Day page ("At Arm's Length"
  vs "With AGM") and the Reporting page.
- **Building engineer and preventative maintenance** have their own section on slide 04, with a
  proposed maintenance schedule for these buildings, an engineer on the team page and contact page,
  and an engineer rate on the Fees page.
- **First 30 days: lease review and NNN review.** Slide 03 runs Day 1-10 handover from the current
  manager, Day 11-30 Lease & NNN Review, then reports and outcome. A block lists the recoverable
  expense categories checked.
- **Removed:** the vacancy scope and $750 interim fee, the marketing broker, "Packaged for Sale", the
  environmental-site section and the Seneca agreement PDF.

## Property data
From the King County Assessor (eReal Property) and King County GIS, pulled 2026-11-20, 2026 valuation
year:

| | 401 Baker Blvd | 405 Baker Blvd |
|---|---|---|
| Parcel | 022310-0085 | 022310-0087 (also addressed 407, 409) |
| Taxpayer | 401 Baker LLC | 405 Baker LLC |
| Building | 18,300 SF, reinforced concrete, 1963 (eff. 2005) | 14,760 SF, masonry, 1965 (eff. 2005) |
| Sections | 10,090 storage warehouse, 4,300 light mfg, 3,910 warehouse office | 7,204 service garage, 5,774 storage warehouse, 1,782 line retail |
| Site | 49,757 SF (1.14 ac) | 33,392 SF (0.77 ac) |
| Zoning / use | TUC-TOD / Warehouse | TUC-TOD / Retail Store |
| Heating / sprinklers | Hot-water radiant / Yes | Space heaters / Yes |
| 2026 value | $3,792,900 (land $2,674,400) | $3,470,200 (land $1,794,800) |

`assets/401-405-baker-blvd-aerial*.jpg` are King County 2025 orthoimagery with the parcel lines drawn
on. The two building photos are the assessor's (400 x 300), and should be replaced with real photography
when it is available.

## Local preview
Serve the folder (the images use root-relative paths), e.g. `python3 -m http.server` and open
`http://localhost:8000`. Deep-link a section with the URL hash, e.g. `#operations`.

## PDF version
Not built yet. The cover's Download PDF button is inert (`aria-disabled="true"`) until it is. Once the
fees are in, run:

```
node scripts/build-pdf.js
```

It writes `AGM-401-405-Baker-Management-Proposal.pdf` to the repo root. Then point the cover button at
that file (see the comment beside it in `index.html`). It needs node, `playwright` with its Chromium, and
python3 with `pypdf` and `reportlab`. The PDF links the Management Agreement button to
`https://401-405-baker-blvd.pages.dev` unless `SITE_URL` is set.

## Deploy to Cloudflare Pages (AGM standard pattern)
1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** → select this repo.
2. Settings: Framework preset **None** · Build command **(empty)** · Build output directory **/**
3. Every push to `main` auto-deploys production; every branch/PR gets its own preview URL.

## Access
No password screen, as on Seneca. Anyone with the link can read it; `_headers` sets `noindex`.

## Analytics (PostHog)
Off until a key is pasted into the marked block in the `<head>` of `index.html`, replacing
`phc_REPLACE_WITH_YOUR_PROJECT_API_KEY`. Events are tagged `proposal: baker-blvd-microsite` so this
proposal can be filtered apart from Seneca in a shared PostHog project. Tracking is otherwise identical
to Seneca: a virtual `$pageview` per section, `tab_click`, `section_time`, autocapture, replays and
heatmaps.

## Operational notes
- **Unfinished content is flagged in the page itself** as amber `[bracketed]` chips (`<span
  class="tbd">`) and dashed "To complete" boxes (`.tbd-note`). `CONTENT-TODO.md` lists every one.
  Before this goes to Ownership, `grep -c 'class="tbd' index.html` must return 0.
- Old Seneca links keep working via the `ALIAS` map (`#letter`, `#contents`, `#technology`,
  `#insurance`, `#contact`).
- No em dashes in any file.
