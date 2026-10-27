# Licensing and attribution

This repository uses a **split license**: the software and the educational content are
licensed differently on purpose.

| What | License | File |
|---|---|---|
| **Source code** — the Flask app, templates, scripts, tooling | **Apache License 2.0** | [`LICENSE`](LICENSE) |
| **Educational content** — question bank, explanations, lessons, misconception library, key-term glossary | **CC BY-NC-SA 4.0** | [`LICENSE-CONTENT`](LICENSE-CONTENT) |
| **Third-party material** | per its own license | this file, below |

## Why the split

The code carries no competitive value — permissive licensing maximises adoption, which is
the point of releasing it. The content is the asset, and a NonCommercial + ShareAlike license
is what stops someone from taking the question bank behind a closed paywall. It is also the
same posture OpenStax itself now uses, so there is no inconsistency between what we ship and
what we build on.

Under **CC BY-NC-SA 4.0** you may use, adapt and redistribute the content freely for
non-commercial purposes, as long as you attribute it, keep it under the same license, and
indicate any changes. Commercial use requires written permission from Mu2 Solutions, LLC.

---

# Third-party attribution

## Fonts — self-hosted, both SIL Open Font License 1.1

The app ships its own copies of the two type families it uses. Nothing is loaded from a
third-party font service, so no visitor's IP address leaves this site to render a page.
Both families are open-source fonts, redistributed here under the same license they carry
upstream, unmodified except for subsetting to the Latin and Latin Extended ranges.

| Family | Used for | Copyright | License | Upstream |
|---|---|---|---|---|
| **Libre Baskerville** | headings, wordmark | © 2012 Pablo Impallari, © 2012 Rodrigo Fuenzalida | SIL OFL 1.1 | <https://github.com/impallari/Libre-Baskerville> |
| **Source Sans 3** | body text, UI | © Adobe | SIL OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |

Files: `static/fonts/*.woff2` (six files: Latin and Latin Extended, roman and italic for
Libre Baskerville, roman for Source Sans 3). Declarations: `static/css/fonts.css`, generated
from the upstream stylesheet with every URL rewritten to a local path.

The OFL permits use, study, modification and redistribution, including bundled with
software, provided the font software is not sold on its own and no modified version uses a
Reserved Font Name. Subsetting for web delivery is a permitted modification; these files
keep their upstream names and are not sold. Full text: <https://scripts.sil.org/OFL>.

## OpenStax — *American Government 2e*

Study material in this project is derived from an OpenStax textbook. Required attribution:

> **American Government 2e**
> Glen Krutz and Sylvie Waskiewicz
> OpenStax, Rice University, 2019
> <https://openstax.org/details/books/american-government-2e>
>
> Licensed under a **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
> <https://creativecommons.org/licenses/by/4.0/>

**Changes made.** Sections of the full text were excerpted and mapped to the four Florida
Civic Literacy Examination domains for use as study and retrieval material. The excerpts are
grouped by domain and used to help students read the underlying material for a topic. Section
text is not modified in substance.

**What this does not cover.** The OpenStax material is study content. It is not assessment
content, and no exam question, answer key or official practice item from OpenStax or from the
Florida Department of Education is reproduced here. All practice questions and explanations
in this project are original work by Mu2 Solutions, LLC.

### A note on editions

OpenStax has since moved its library to **CC BY-NC-SA** for newly released and updated
editions. *American Government 2e* was published under **CC BY 4.0**, and Creative Commons
licenses are irrevocable — so the grant above is the one that applies to this material. If
this project ever refreshes its source material to a later edition, that edition's license
(and the NonCommercial restriction that comes with it) will apply and this file must be
updated first. **Do not swap the source text without re-reading this section.**

## Florida Department of Education

This project references Florida social studies **benchmark codes** (e.g. `SS.7.CG.3.9`) as
identifiers for mapping topics to state standards. Benchmark codes and standards are published
by the state for public use.

FLDOE-authored document **text** — including the competencies described in the *Supplemental
Guide for the Florida Civic Literacy Examination* — is **not** reproduced in this project. The
FLDOE states that permission is not granted for reproduction or commercial distribution of its
copyrighted materials without written authorisation. All student-facing explanations,
definitions and feedback in this project are written in our own words.

## United States Government documents - public domain

Chapter 18 (*Appendices*) reproduces primary documents of the United States government, which
are in the public domain and are not subject to copyright in the United States:

- the **Declaration of Independence**
- the **Constitution of the United States**, including the Bill of Rights and subsequent amendments
- **Federalist Papers** No. 10 and No. 51
- the **Electoral College** vote allocation
- selected **Supreme Court** decisions

These are reproduced for study purposes and may be freely reused. Any Mu2-authored notes,
headings or explanations surrounding them are licensed as content under CC BY-NC-SA 4.0, as above.

## Mu2 Solutions original content

Chapter 20 (*Mu2 Original Content*) is **written by Mu2 Solutions, LLC** and is **not derived
from OpenStax** or from any other third party. It carries the same content license as the rest
of the educational material: **CC BY-NC-SA 4.0** (see [`LICENSE-CONTENT`](LICENSE-CONTENT)).

Published so far:

- **20.1. Sources and Types of Law** - written to cover benchmark `SS.7.CG.3.10`, which the
  OpenStax textbook does not address: historical codes of law (Hammurabi, the Roman Twelve
  Tables, Magna Carta 1215, the English Bill of Rights 1689); the five sources of law (natural,
  constitutional, statutory, common, case); and the comparison of civil, criminal, constitutional
  and military law, including who brings the case, the standard of proof, and the consequence.

Original content is written in our own words. The source text of each item is version-controlled
under `data/mu2-original/` so that the published text and its provenance can be compared.

## Everything else

Fonts, icons and any other third-party assets remain the property of their respective owners
and are governed by their own licenses.

---

## Reporting a problem

If you believe material here is misattributed or used outside its license, please open an
issue and it will be corrected promptly.
