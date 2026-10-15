# Quality floor

Every source skill holds a version of this floor. It's the work a careful designer ships without mentioning it. Each item is a check on the built result, not an intention, and `scripts/lint_tells.py` catches the mechanical ones.

## Contents

1. Contrast and color
2. Focus and keyboard
3. Semantics and accessibility
4. Forms
5. Typography
6. Layout and responsive
7. Images and media
8. Content handling
9. States and copy
10. Browser surfaces and theming
11. Performance

## 1. Contrast and color

- Body and placeholder text at least 4.5:1 against its background. Large text (24px, or 19px bold) and the boundaries of inputs and controls at least 3:1.
- Secondary text on a colored surface is tinted from that surface's hue or the foreground, never a flat grey. Grey on color reads muddy and usually fails contrast.
- Running text is in the full ink color. A page set in soft grey reads unfinished.
- Color never carries meaning alone. Errors, status, and chart series also differ by icon, label, or shape.
- Use semantic color tokens in components, not raw hex values, so themes and dark mode work.

## 2. Focus and keyboard

- Every interactive element shows a visible focus state, using `:focus-visible` so a mouse click doesn't draw a ring.
- Never `outline: none` (or Tailwind `outline-none`) without a replacement focus style.
- Compound controls use `:focus-within` so the whole group shows focus.
- Sticky headers, footers, and overlays don't cover the focused element. Give heading anchors `scroll-margin-top`.
- Everything works from the keyboard, in a sensible order. Drag, swipe, and pinch actions have a click or key alternative.
- Add a skip link to the main content on pages with navigation.

## 3. Semantics and accessibility

- `<button>` for actions, `<a>` for navigation. No `<div>` or `<span>` with a click handler.
- Icon-only buttons get `aria-label`. Decorative icons get `aria-hidden="true"`.
- Headings are hierarchical, one `<h1>` per page, and never skip levels for styling.
- Async updates (toasts, inline validation) are announced with `aria-live="polite"`.
- Use semantic HTML before ARIA.
- Touch targets are at least 44 by 44px, with at least 8px between neighbors.

## 4. Forms

- Every input has a visible label. A placeholder is not a label.
- Use the right `type` and `inputmode` (`email`, `tel`, `url`, `number`), plus `autocomplete` and a meaningful `name`.
- Inputs are at least 16px on mobile, or iOS zooms the page on focus.
- Never block paste.
- Errors appear next to the field, say what's wrong and how to fix it, and focus moves to the first error on submit.
- The submit button stays enabled until the request starts, then shows progress.
- Warn before leaving a page with unsaved changes.

## 5. Typography

- One or two typefaces. If two, make them clearly different. Five sizes on a page is the ceiling, and two or three should do the visible work.
- Load every weight and style you use. Browsers fake missing bold and italic, and the result looks wrong.
- Body text 16px or more. Weights below 400 only at 28px and up.
- Line length 45 to 75 characters for body text.
- Line height: about 1.1 for display, 1.2 to 1.3 for headings, 1.4 to 1.6 for body. Use unitless values. Anything that wraps to three or more lines needs at least 1.4.
- Tracking: display type slightly tight (-0.01 to -0.03em), body at 0, and small uppercase labels slightly open (about 0.05em) if you use them at all.
- `text-wrap: balance` on headings and short descriptions; `text-wrap: pretty` on paragraphs.
- `font-variant-numeric: tabular-nums` on prices, counters, timers, and number columns so digits don't shift.
- Real punctuation: `…` not `...`, curly quotes, non-breaking spaces between numbers and units (`10&nbsp;MB`).
- Left-aligned by default. Center at most one moment on a page. Never justify interface text.
- Heading sizes descend with level. A subordinate heading never outweighs its parent.

## 6. Layout and responsive

- One grid and one pair of page margins, used everywhere.
- The gap between sections is clearly larger than any gap inside one. More space above a heading than below it, so the heading belongs to what follows.
- Works from 390px wide up, with no horizontal scroll. The phone layout is its own composition, not the desktop squeezed.
- Never `user-scalable=no` or `maximum-scale=1`.
- Full-height sections use `min-height: 100dvh`, not `100vh`, which jumps on mobile Safari.
- Full-bleed layouts respect `env(safe-area-inset-*)`.
- Use CSS grid and flex for layout, not JavaScript measurement.
- Nested rounded surfaces with an even inset: outer radius equals inner radius plus padding.

## 7. Images and media

- `<img>` has explicit `width` and `height` to prevent layout shift, and `alt` text (`alt=""` if decorative).
- Below-the-fold images use `loading="lazy"`; the main above-the-fold image gets `fetchpriority="high"`.
- Use compressed video (`<video autoplay muted loop playsinline>`) instead of animated GIFs, with a poster frame.
- Same crop ratios and the same treatment across a set of images.
- Nothing sits on top of a headline or body text. Text on a photo gets a neutral scrim.
- Every found or stock image is credited and never presented as the client's own product, place, or people.

## 8. Content handling

- Containers handle long content: truncation, line clamping, or `overflow-wrap: break-word`. A truncated value has a way back to the full text (tooltip, expand, detail view).
- Flex children that hold text need `min-width: 0` so truncation works.
- Test with short, average, and very long real content, including user-generated text.
- Empty strings and empty lists render a designed empty state, not broken UI.

## 9. States and copy

- Every interactive element has hover (behind `@media (hover: hover)`), active, focus, and disabled states. Interactive states are more prominent than the resting state.
- Loading, empty, and error states exist for every async view. Skeletons match the layout they replace.
- Buttons say exactly what happens: "Save changes", not "Submit". An action keeps its name through the flow: the "Publish" button produces a "Published" toast.
- Errors name the problem and the fix, in the interface's voice. They don't apologize and they're never vague.
- Name things by what users understand, not how the system is built.
- Destructive actions get a confirmation or an undo window.

## 10. Browser surfaces and theming

The parts you didn't draw still carry the design. These are the cheapest signal that a page was built rather than assembled, and the ones most often skipped.

- Style `::selection`, focus rings, the caret color, link underline offset, and scrollbars from the palette.
- Dark themes set `color-scheme: dark` on `<html>` so native controls and scrollbars match.
- `<meta name="theme-color">` matches the page background.
- Native `<select>` gets explicit background and text colors (Windows dark mode).
- Disable transitions during a theme switch so every color doesn't animate at once.

## 11. Performance

- Animate `transform` and `opacity`. Never `transition: all`; list the properties.
- Virtualize lists longer than about 50 items.
- Preload critical fonts with `font-display: swap`; preconnect to font and asset hosts.
- No layout reads (`getBoundingClientRect`, `offsetHeight`) during render.
- Grain and noise overlays go on a fixed, non-scrolling layer, never on scrolling containers.
