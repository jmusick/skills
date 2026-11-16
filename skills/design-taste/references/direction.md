# Direction

Use this in build mode when no other skill has set a direction, and in polish when the user asks for a redesign rather than a cleanup.

1. **Name the subject, the audience, and the one job of the surface.** If the request is vague, decide and state your reading in one line. Ask only when a missing fact blocks the work, such as no product name.
2. **Inventory the subject.** List 6 to 10 things that belong to this client and no competitor: its name and what it means, its place, its materials and colors, the numbers in the brief, the constraint it lives with, its rituals and hours, the printed things of its world (a ticket, a label, a manual). Distinctive choices come from this list. Test each idea by putting the nearest competitor's name in it; if the idea still works, it belongs to the category, not the client.
3. **Know what kind of surface it is.** Marketing and portfolio pages can be expressive, and the visitor must know what this is and what to do within seconds. Working screens (dashboards, settings, editors) favor scannability, consistency, and density, with personality in precise details. Reading surfaces (docs, articles) favor measure, structure, and wayfinding. Pick light or dark from where and under what light people use it, not from the category.
4. **Declare the system before code.** Write a short plan: 4 to 6 named colors with hex values and roles; one or two typefaces chosen by "Choosing and pairing type" below, each with its role and the sentence saying why it fits, and a scale of five sizes or fewer; a spacing base; one radius strategy decided once; how surfaces separate (tone steps, shadows, or borders); and the one motion moment, if any. Sketch the first viewport as an ASCII wireframe. Save it to the project's design doc (`DESIGN.md` if none exists) so later sessions follow the same decisions.
5. **Check the plan against the default.** Ask whether you'd have produced the same plan for any similar brief. Revise every part that would, and say what you changed and why.
6. **Spend boldness in one place.** One element is the memorable thing. Keep everything around it quiet and disciplined.

## Choosing and pairing type

Type advice agrees on method and disagrees on names, so this gives the method and no list of faces or pairs. Use it in build mode, and in polish when a face is missing a reason. If the brand already has its faces, keep them (the brief wins) and run only the checks in steps 3 to 7 below, reporting what fails.

### Choose the main face

1. **Start from the subject, not the catalog.** From the inventory in step 2, name the feeling the type should give this audience and the era or world it belongs to; the printed things of that world often show it. Readers react to how type feels before they read it, and those associations differ between audiences and change over time. Feeling narrows the field; the checks below decide.
2. **Fit the face to the amount of text and its size.** Body text and interface labels need a workhorse: a generous x-height, moderate stroke contrast, open spacing, and plain shapes. Expressive faces (high contrast, swashes, quirks, scripts) belong at display sizes in short runs. Code and columns of data want monospace.
3. **Test legibility on the glyphs that give a face away.** Set `Il1`, `O0`, `a`, `g`, and the numerals at body size. If I, l, and 1 blur together, or the `a`, `g`, and figures look careless, don't use it for text.
4. **Check the family covers the job.** Text needs at least regular, italic, bold, and bold italic. More weights, widths, or optical sizes (often in one variable font) let one family do what would otherwise take two. Check for the figures the page needs (tabular for prices and tables, oldstyle for numbers in paragraphs) and for small caps or fractions if the content uses them.
5. **Check language coverage past the brief.** At least Western European Latin, and extended Latin where you can. User input, a CMS, and browser auto-translate put characters on the page you didn't write, and each missing glyph falls back to a different face. For other scripts, choose a family drawn across them.
6. **Check the files you'll serve, not the specimen.** A CDN or "lite" build can lack the glyphs, weights, or OpenType features the specimen shows. Set real text in the served files and look at the spacing and kerning.
7. **Confirm the license covers this use** (web, app, scale). If you can't confirm it, say so in the report rather than assume.
8. **Run the default test.** Would you have picked this face for any similar brief? If so, and steps 1 and 2 don't argue for it, keep looking. Write one sentence in the plan saying why this face fits this subject. The choice is half the work: size, spacing, and arrangement carry as much of the feeling as the letterforms.

### Pair a second face

1. **Start with one family.** Use its weights, widths, italics, optical sizes, case, size, and tracking for contrast before you reach for another face. Many good pages use one family.
2. **Add a second face only for a job the first can't do,** and name that job: data or code beside prose, a tone the first lacks, a weight or italic it doesn't have (rather than letting the browser fake one), or characters it doesn't cover. A third face needs the same reason and is rarely right; four almost never.
3. **Make the pair different enough, not too different.** Two faces so alike they could be mistaken for each other read as an error. Two that share nothing compete. Match at least one trait, such as x-height, stroke contrast, width, or mood, and differ clearly in at least one, such as structure (serif and sans, proportional and mono) or tone. The more traits they share, the closer the relation. Serif with sans is the safe default, not a rule: two serifs can work, and lower contrast often works better than high.
4. **Mind the era.** Faces from different historical periods carry different associations; pair across periods on purpose, not by accident.
5. **Use a shortcut when one fits.** A superfamily (a serif, sans, slab, or mono drawn on one skeleton) shares proportions, spacing, and x-height, so it rarely needs an outside face. Two faces from the same designer or foundry often share a hand. Check the traits anyway: the same maker doesn't guarantee them.
6. **Give each face one fixed job,** the same everywhere: headings and body, content and peripheral text (captions, footers, line numbers), prose and data. Switch faces only at a block boundary, never inside a paragraph.
7. **Look at the pair before committing.** Set a heading over a paragraph at real sizes, with real copy, and screenshot it at both widths in the critique loop. If the faces can't be told apart at a glance, or one fights the other, change one of them.
