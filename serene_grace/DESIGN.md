---
name: Serene Grace
colors:
  surface: '#f7faf9'
  surface-dim: '#d7dbda'
  surface-bright: '#f7faf9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f3'
  surface-container: '#ebeeed'
  surface-container-high: '#e6e9e8'
  surface-container-highest: '#e0e3e2'
  on-surface: '#181c1c'
  on-surface-variant: '#414844'
  inverse-surface: '#2d3131'
  inverse-on-surface: '#eef1f0'
  outline: '#717974'
  outline-variant: '#c1c8c3'
  surface-tint: '#426657'
  primary: '#3f6355'
  on-primary: '#ffffff'
  primary-container: '#587c6d'
  on-primary-container: '#f5fff8'
  inverse-primary: '#a8cfbd'
  secondary: '#486456'
  on-secondary: '#ffffff'
  secondary-container: '#caead8'
  on-secondary-container: '#4e6b5c'
  tertiary: '#4b605c'
  on-tertiary: '#ffffff'
  tertiary-container: '#637975'
  on-tertiary-container: '#f4fffc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c4ebd9'
  primary-fixed-dim: '#a8cfbd'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#2a4d40'
  secondary-fixed: '#caead8'
  secondary-fixed-dim: '#aecebc'
  on-secondary-fixed: '#042015'
  on-secondary-fixed-variant: '#314c3f'
  tertiary-fixed: '#d0e7e2'
  tertiary-fixed-dim: '#b5cbc6'
  on-tertiary-fixed: '#0a1f1c'
  on-tertiary-fixed-variant: '#364b47'
  background: '#f7faf9'
  on-background: '#181c1c'
  surface-variant: '#e0e3e2'
typography:
  headline-lg:
    fontFamily: Gowun Dodum
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Gowun Dodum
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Gowun Dodum
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Gowun Batang
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Gowun Batang
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Gowun Batang
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-lg:
    fontFamily: Gowun Batang
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  label-md:
    fontFamily: Gowun Batang
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
  headline-lg-mobile:
    fontFamily: Gowun Dodum
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  margin-page: 20px
  gutter-card: 16px
  stack-gap: 24px
  component-padding-x: 16px
  component-padding-y: 12px
---

## Brand & Style
This design system is crafted for a contemporary Korean church community, blending traditional spiritual values with a modern, accessible digital experience. The brand personality is serene, welcoming, and organized, aiming to evoke a sense of peace and belonging.

The aesthetic follows a **Modern/Corporate** hybrid with strong **Minimalist** and **Traditional** influences. It prioritizes clarity and breathability, using generous whitespace to allow theological content and community announcements to feel significant rather than cluttered. The visual language is defined by soft edges and a refined, card-based architecture that provides a tangible, organized feel to the digital bulletin.

## Colors
The palette is rooted in a "Sage Green" spectrum, symbolizing growth, life, and peace. 

- **Primary:** A grounded sage green used for headers, primary actions, and brand-defining accents.
- **Secondary & Tertiary:** Softer tints of the primary hue, used for decorative elements, secondary buttons, and subtle background shifts.
- **Neutral:** A very light, mint-tinted off-white serves as the main background color to reduce eye strain and provide a softer feel than pure white.
- **Surface:** Pure white (#FFFFFF) is reserved strictly for cards and elevated containers to make them pop against the neutral background.

## Typography
The system utilizes **Gowun Dodum** for headlines to provide a contemporary, friendly typographic voice. For body text and system labels, **Gowun Batang** ensures maximum legibility and a classic, elegant tone that honors traditional script styles while remaining perfectly readable on digital screens.

Hierarchy is maintained through weight and size rather than color shifts. Scripture quotes should be set in `body-lg` with italic styling (where supported) or slightly wider margins to denote their sacred nature.

## Layout & Spacing
The layout uses a **Fixed Grid** philosophy centered on a single-column vertical stack for mobile, and a multi-column staggered card layout for larger screens. 

- **Rhythm:** A 4px/8px base-unit system is used to ensure mathematical harmony.
- **Card-Based:** Every piece of information (Order of Service, Sermon Notes, Announcements) is encapsulated in a card.
- **Safe Areas:** Standard page margins are 20px on mobile to allow cards to feel substantial without touching the edge of the device frame. 
- **Stacking:** Cards are separated by a 24px vertical gap to signify a change in topic or service segment.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** combined with **Ambient Shadows**. This mimics a physical church bulletin laid on a soft surface.

- **Level 0 (Background):** The `neutral` color (#F6F9F8).
- **Level 1 (Cards):** Pure white background with a very soft, diffused shadow (Blur: 20px, Y: 4px, Color: 6B9080 at 8% opacity). This "tinted shadow" keeps the design feeling warm and integrated with the sage palette.
- **Level 2 (Interactive):** When a user interacts with a card or button, the shadow deepens slightly and the element scales by 1% to provide tactile feedback.

## Shapes
The shape language is consistently **Rounded**, avoiding sharp corners to maintain the welcoming and gentle brand personality.

- **Cards:** Use `rounded-xl` (1.5rem / 24px) to create a soft, friendly container.
- **Buttons & Inputs:** Use `rounded-lg` (1rem / 16px) for a distinct but harmonious look.
- **Chips/Badges:** Use a full pill shape for categorical tags (e.g., "Sermon", "Event", "Notice").

## Components
### Buttons
Primary buttons use the `primary_color_hex` with white text. Secondary buttons use `tertiary_color_hex` with the primary green text. All buttons have a medium-weight label and significant horizontal padding.

### Cards
Cards are the primary container. They must have a white background, the defined Level 1 shadow, and 24px internal padding. Card headers should use `headline-sm`.

### Sermon Notes (Input Fields)
Input fields within the "Sermon Notes" section should be "ghost style"—no background, just a subtle bottom border in `secondary_color_hex`. This mimics a physical notebook, encouraging parishioners to fill in the blanks.

### Chips & Tabs
Navigation tabs (e.g., Sunday, Connect, Give) should use a pill-shaped background. The active state is indicated by the `primary_color_hex` background, while inactive states use the `neutral_color_hex`.

### Lists
Lists (like the Order of Service) should use a subtle horizontal separator in `tertiary_color_hex` with 1px thickness, stopping 16px before the card edge to maintain a clean look.