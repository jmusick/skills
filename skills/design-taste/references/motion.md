# Motion

Motion is for the user, not for the page. Values marked "exact" are worth copying as given. The rest are ranges to judge by eye.

## Contents

1. Decide whether to animate
2. Easing
3. Duration
4. Recipes
5. Entrances and exits
6. Reduced motion
7. Performance

## 1. Decide whether to animate

Ask two questions, in order.

**How often will the user see it?**

| How often | Decision |
| --- | --- |
| Hundreds of times a day (keyboard shortcuts, command palette, typing) | No animation. Ever. |
| Tens of times a day (hovers, list navigation, tab switches, row hovers) | None, or 150ms or less on `opacity` or `background-color` |
| Occasionally (menus, modals, drawers, toasts) | Standard animation |
| Rarely (first load, onboarding, success, empty states) | Room for one expressive moment |

Never animate a keyboard-initiated action. It's repeated so often that any motion makes the interface feel slow.

**What is it for?** Valid answers:

- **Feedback:** a button scales down on press, so the user knows the interface heard them.
- **State change:** a button morphs to show it's saving, then saved.
- **Spatial continuity:** a toast leaves the way it came, so swipe-to-dismiss makes sense.
- **Explanation:** a marketing animation shows how a feature works.
- **Softening a jump:** an element that appears or disappears instantly can feel broken.

If the only answer is "it looks nice" and the user sees it often, don't animate. Every animated change also leaves a static cue (a color, icon, or label); motion is never the only feedback.

## 2. Easing

| Situation | Easing |
| --- | --- |
| Entering or exiting | Strong ease-out |
| Moving or morphing on screen | Strong ease-in-out |
| Hover and color changes | `ease` |
| Constant motion (marquee, progress) | `linear` |
| Anything else | Strong ease-out |

Built-in CSS easings are too weak to feel intentional. Use custom curves:

```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* menus, popovers, entrances */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* things moving across the screen */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like sheets and drawers */
}
```

`cubic-bezier(0.2, 0, 0, 1)` is a gentler ease-out that also works well. Pick one family and use it everywhere.

**Never use `ease-in` for UI.** It starts slowly, which delays movement at the exact moment the user is watching. A 300ms dropdown with `ease-in` feels slower than the same 300ms with ease-out.

**Springs** suit drags, gestures that can be interrupted, and things that should feel physical. They keep their velocity when interrupted, where CSS animations restart. Keep bounce at 0 for ordinary UI, and at most 0.1 to 0.3 for playful or drag-to-dismiss interactions.

```js
{ type: "spring", duration: 0.3, bounce: 0 }
```

## 3. Duration

| Element | Duration |
| --- | --- |
| Button press feedback | 100 to 160ms |
| Tooltip, small popover | 125 to 200ms |
| Dropdown, select, menu | 150 to 250ms |
| Modal, drawer, sheet | 200 to 400ms |
| Marketing or explanatory sequences | Longer is fine |

Keep interface animation under 300ms. Faster feels more responsive, and perceived speed matters as much as real speed: a fast spinner makes the same load feel shorter.

Once one tooltip is open, open neighboring tooltips instantly with no delay and no animation.

## 4. Recipes

**Press feedback.** Pressable elements scale to between `0.96` and `0.98` on `:active`, over about 150ms with ease-out. Disabled elements never scale.

```css
.button { transition: transform 150ms var(--ease-out); }
.button:not(:disabled):active { transform: scale(0.97); }
```

**Never animate from `scale(0)`.** Nothing in the world appears from nothing. Start near `0.95` with `opacity: 0`.

**Origin-aware popovers.** Menus, popovers, and tooltips scale from their trigger, not their center. Modals stay centered because they aren't anchored to anything.

```css
.popover { transform-origin: var(--transform-origin); } /* set by the component library */
```

**Transitions for interactive state, keyframes for one-off sequences.** A transition retargets when the user reverses mid-flight (opens, then quickly closes). A keyframe animation runs a fixed timeline and can't reverse smoothly.

**Blur bridges a crossfade.** When one state replaces another in place (an icon swap, copy to copied), a small blur (about 4px) during the crossfade makes two objects read as one transformation.

**Icon swaps** on infrequent state changes: crossfade with scale from about `0.25` to `1`, opacity `0` to `1`, and blur `4px` to `0`.

**Skip animations on first render.** Default states shouldn't animate in on mount. Only intentional entrances (a staged hero) play on load.

**Hover only where hover exists.** Wrap hover styles in `@media (hover: hover)` so a tap on a phone doesn't leave a stuck hover state.

## 5. Entrances and exits

- **One orchestrated moment** on a page (one load sequence or one reveal) lands better than effects scattered across every section. The same fade-and-rise on every section is a tell.
- **Content is visible by default.** If the script fails or is slow, nothing stays hidden.
- **Stagger only infrequent entrances,** and only where order shows hierarchy: title, then text, then actions, 60 to 100ms apart, each rising 12 to 24px with opacity over about 300ms. Never stagger routine interactions.
- **Exits are shorter and smaller than entrances:** about 150ms, a small fixed offset, never the full height of the container. Slide fully out only when the destination means something (a drawer closing into its edge). Remove instantly when motion adds no information.

## 6. Reduced motion

Every movement has a `prefers-reduced-motion` path. Keep the content and the state change, drop the travel. Prefer a short opacity crossfade over removing the element instantly.

```css
@media (prefers-reduced-motion: no-preference) {
  .reveal { transition: transform 300ms var(--ease-out), opacity 300ms var(--ease-out); }
}
@media (prefers-reduced-motion: reduce) {
  .reveal { transition: opacity 150ms linear; transform: none; }
}
```

Autoplaying motion longer than 5 seconds next to other content needs a pause control, and decorative loops stop under reduced motion.

## 7. Performance

- Animate `transform`, `opacity`, and `filter` only. Never `top`, `left`, `width`, or `height`.
- Name the properties: `transition: transform 200ms, opacity 200ms`. Never `transition: all`; it animates things you didn't mean to and costs performance.
- Add `will-change` only after you see first-frame stutter, and name the property you animate. Never `will-change: all`.
- `scale()` scales children too. Scale a wrapper if the text inside shouldn't blur or grow.
- Disable transitions during a theme switch, or every color animates at once and the switch smears.
- Check motion at 10% speed in the browser's animation panel before calling it done.
