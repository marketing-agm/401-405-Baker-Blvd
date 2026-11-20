# 401 & 405 Baker Blvd: content status

Draft started 2026-11-20 from the Seneca proposal. Every open item below shows in the page as an amber
`[bracketed]` chip or a dashed "To complete" box.

## Outstanding

| Item | Where | Who |
|---|---|---|
| Management fee (% of gross rents), monthly minimum per property, onboarding fee per property | Slide 08, fee card 1 | Herman |
| Building engineer hourly rate | Slide 08, fee card 2 | Herman |
| Building engineer name, direct line and email | Slide 02 (Supporting Team), slide 09 (Contact) | Leary |
| Tenants, suites and lease expirations for each building | Slide 01, Tenancy & Lease Status | Leary / Ownership |
| Draft management agreement PDF (one per LLC, same terms) and link on the button | Slide 09, Ready to Proceed | Makenzie |
| Cover letter review | Cover | Leary (said they will assist) |
| Build the PDF and enable the Download PDF button | Cover | After the above |

## Assumptions to confirm
- **Property manager.** Cindy Miller is named as the manager, carried over from Seneca. Change if
  another manager is assigned.
- **Both buildings are leased on NNN terms.** Taken from the email's request to review NNN charges.
  Neither building appears in current Tukwila for-lease listings; both had marketing listings in 2024
  and tenant-improvement permits in 2024-25.
- **The preventative maintenance schedule** (slide 04) is a proposed schedule from the assessor data
  (hot-water radiant heat at 401, space heaters at 405, both sprinklered, low-slope roofs visible in the
  2025 aerial). It is set after the engineer's first walk.
- **Sample owner report** (slide 05) is from a fictional property, signed by the Studio's demo manager
  and watermarked SAMPLE. Its narrative and notes are illustrative. Swap in a redacted real report only if
  Ownership asks for one.
- **Track Record** (Pacific Business Park case study, Mount Si, Clover) is unchanged from Seneca.

## Release check
- `grep -c 'class="tbd' index.html` returns 0
- Rebuild the PDF and enable the cover button
- No em dashes: `python3 -c "print(open('index.html',encoding='utf-8').read().count(chr(0x2014)))"`
