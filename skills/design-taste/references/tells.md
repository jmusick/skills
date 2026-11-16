# Tells: the dated registry

A tell is a device that makes a page read as generated. Most began as good ideas on good sites. They became tells by being produced by default, everywhere, without a reason. That is why this registry is dated, and why it gives procedures instead of replacement products: every published "use this instead" list (fonts, palettes, components) became the next wave of tells.

`scripts/lint_tells.py` catches the mechanical ones. The rest need eyes on a screenshot.

Every entry is a default to avoid where the brief leaves the choice open. If the user or the brand asks for it, keep it and note it in the report.

## Contents

1. First wave (2023 to 2024)
2. Second wave (2025)
3. Third wave (2025 to 2026): the fix that became the look
4. Structural tells
5. Copy tells
6. Motion tells
7. What to do with the space

## 1. First wave (2023 to 2024)

| Tell | Why it reads as generated | Do instead | Fine when |
| --- | --- | --- | --- |
| Violet or indigo gradients on the hero, buttons, and glows | The single most common default in early generated UI | Flat color from the declared palette, or a real photograph | The brand's own color is violet |
| Gradient-filled headline text | Decoration standing in for hierarchy | Solid ink; emphasis from size and weight | Almost never |
| Glowing or gradient "Get started" button | Draws attention with effect instead of placement | A flat button named for what it does | Never |
| Soft grey shadow (`rgba(0,0,0,.1)`) under every card | One elevation applied to everything means elevation says nothing | A tone step between surfaces; shadows only on what truly floats (menus, dialogs) | The shadow marks real elevation |
| Three identical feature cards, each with an icon in a rounded square | The stock container for "features" regardless of content | A section composed for this content: a list, a comparison, a demonstration, a picture with text | The content is truly a set of equal peers, and the cards aren't the page's whole structure |
| Emoji as icons or bullets | Cheapest available icon system | One icon library, one stroke weight, or words | The brand voice is truly playful and the user asked |
| The same typeface on every generated page | Training-data default | A face chosen for this subject | The brand uses it |

## 2. Second wave (2025)

| Tell | Why it reads as generated | Do instead | Fine when |
| --- | --- | --- | --- |
| Eyebrow or kicker: tiny tracked uppercase label above every heading | Template chrome that carries no information | Fold the information into the heading or first sentence, or delete it | Never as a repeated pattern |
| Pill badge above the hero headline ("New", "Beta", "Introducing") | Borrowed launch-page chrome | Say it in the supporting sentence | There really is a new release and it's the news |
| One word of a headline in italic serif, a color, or underlined | Emphasis by formula | One face, one color; the words carry the emphasis | The brand's wordmark does it |
| Bento grid of rounded tiles as the feature section | The 2025 replacement for three cards, now just as common | A composed section; tiles only when the content is truly tiled, with strict sizes | A gallery or dashboard of real items |
| Near-black ground with one neon accent and glowing edges | "Developer tool" costume | A dark palette chosen from the use scene, no glow | The product really lives in a dark room |
| Floating rounded pill navigation with blur | Copied from a few famous sites | A plain bar: wordmark, three to five links, one action | The brand's existing site already uses it |
| Fake dashboard hero built from grey bars and donut charts | Pretends to show a product that isn't shown | A real interface fragment, cropped, or no image | Never |
| Decorative status dot ("Available for work", pulsing "live") | Motion and color with no state behind it | Remove it, or wire it to real state | The status is real and live |
| Glass panels, backdrop blur | Texture standing in for structure | Opaque surfaces one tone step from the ground | One specific effect, such as a sheet over live content |

## 3. Third wave (2025 to 2026): the fix that became the look

The remedy published for the first two waves was "warm it up and make it editorial". Models adopted it wholesale and it's now the most recognizable generated look.

| Tell | Why it reads as generated | Do instead | Fine when |
| --- | --- | --- | --- |
| Warm cream ground (near `#F4F1EA`) with a terracotta, rust, or clay accent (near `#D97757`) | The default "warm and human" palette; the accent is also Claude's own interface color | Take warmth from the subject's real materials, a deep ink, a photograph, or a full warm field | The subject's own colors are exactly these |
| High-contrast or soft serif display as the shortcut to "premium" | Signals taste without making a choice | A face chosen for this subject, of whatever class | The subject calls for it and you can say why |
| Oversized italic serif headline | Same | As above | Same |
| Broadsheet cosplay: hairline rules everywhere, zero radius, dense columns, small tracked mono labels | The editorial look applied to subjects that aren't publications | Structure from space, scale, and tone | It's actually a publication |
| Tinted near-black (`#0B0B0B`, `#111`) standing in for black by habit | A reflex, not a palette decision | Pick the darkest color on purpose, as part of the palette | It was chosen, and it's used consistently |
| Bookish, family, or child subjects rendered as cream, serif, and lamplight | The subject's softest, most obvious rendition | The subject's saturated materials: book cloth, thread, toys, paint | The brief asks for exactly that warmth |

## 4. Structural tells

| Tell | Do instead |
| --- | --- |
| Stock section order: hero, logos, three features, testimonial, pricing, call to action | Write the page as claims with proof, one line per section, and let the claims decide which sections exist and in what order. Delete any section with no claim. |
| Centered headline, subtitle, two buttons, screenshot below | Open with the most characteristic thing in the subject's world, at the scale it has in life. |
| Headline of three or more lines at display size; a full sentence set as a headline | A title of about five words; the rest goes in the supporting sentence. About 32 characters fits two lines almost everywhere. |
| Every section in the same layout family | Neighboring sections differ in composition. |
| A distinctive first screen followed by stock blocks | Carry the idea into every section, including pricing, FAQ, and footer. |
| Big number, small label, supporting stats, gradient accent as the hero | Only if a number truly is the most important fact, and then with nothing decorative around it. |
| Section numbers 01 / 02 / 03 | Order shown by position, size, or the words. A real `<ol>` when the order matters to the reader. |
| Footer as a sitemap of every link | A designed close: the name, the one action, the essentials. |
| A modal for a task that needs neither interruption nor protected focus | Inline, or a new page. |
| Nested cards | One level of container, or none. |

## 5. Copy tells

| Tell | Do instead |
| --- | --- |
| Elevate, seamless, unleash, supercharge, next-gen, empower, revolutionize | Say what the thing does, in the user's words. |
| Meta strings joined with middle dots, `WORD — fragment` labels | Plain sentences, or a real list. |
| `→` appended to every link and button | A label that says what happens: "Save changes", not "Submit →". |
| "Scroll to explore", bouncing chevrons, "Learn more" next to every primary action | Content that pulls the reader on; one primary action. |
| Performative labels: "Field notes", "On our desks", "Quietly trusted by" | Plain section names. |
| Generic names (Acme, John Doe, Nexus) and round invented numbers (99.9%, 10x, 50,000+ teams) | Real names and numbers from the brief, or visible placeholders. |
| Agency micro-meta: local time, coordinates, weather, version stamps | Remove. |
| Title Case or ALL CAPS on everything | Match the project's convention; sentence case is the safe default. |

## 6. Motion tells

| Tell | Do instead |
| --- | --- |
| Fade-and-rise on every section | One orchestrated moment; content visible by default. |
| Hover lift and shadow on every card | Hover feedback only on things that are actually clickable, and quiet. |
| Perpetual loops: shimmer, pulse, float, typewriter | Motion that answers an action or shows a change of state. |
| Animating keyboard-driven actions | Instant. |
| Elements growing from `scale(0)` | Start near `0.95` with opacity. |
| `ease-in` on menus and popovers | Strong ease-out. |
| Custom cursors, parallax on everything | Remove unless it is the page's one idea. |

## 7. What to do with the space

Removing a tell leaves a gap. In taste-skill's blind comparisons, a page that lost its labels, rules, and cards and gained nothing in their place lost to a busier page that kept its tells. Fill the gap with, in order of preference:

1. **Scale.** Make the main thing larger. Strong pages use two or three sizes that do the visible work: one very large, one small, little in between.
2. **The full content.** Every section the brief asks for, complete: the whole menu with prices, each room with its details, an answer for each real question.
3. **A real picture of the subject's world.** The project's own photographs or interface first; then honest found pictures (open archives, museum collections, maps) credited on the page and never presented as the client's own; then drawings made for this subject in its colors.
4. **A field of flat color.** A section may change the whole ground color.
5. **Deliberate empty space,** at most once per page.

Never a placeholder icon, an abstract blob, or another ornament.
