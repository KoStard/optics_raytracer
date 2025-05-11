# UI Naming Proposals for Ray Groups

This document explores various approaches to make ray group names more user-friendly while preserving their informative nature.

## Current System (For Reference)
```
2nd_refraction_at_object_0
hit_points_at_object_0
missed_rays
1st_refraction_through_lens_0
hit_points_at_lens_0
```

## Proposal 1: Descriptive with Emojis
Combines visual indicators with clear descriptions

### Ray Paths
- 🌟 Primary Rays
- 🔄 First Reflection
- 🔄 Second Reflection
- ❌ Missed Rays

### Interaction Points
- 📍 Rectangle Hit Points
- 📍 Circle Hit Points
- 🎯 Lens 1 Hit Points
- 🎯 Lens 2 Hit Points

**Pros:**
- Instantly recognizable categories with emojis
- Clear, plain language descriptions
- Visual hierarchy through emoji use

**Cons:**
- Emoji interpretation might vary across platforms
- Could look too casual for scientific software

## Proposal 2: Physics-Style Notation
Using physics-inspired notation that feels natural to optics users

### Ray Paths
- R₀: Primary Rays
- R₁: First Reflection
- R₂: Second Reflection
- R𝕏: Missed Rays

### Interaction Points
- P₁(rect): Rectangle Points
- P₁(lens): Lens 1 Points
- P₂(lens): Lens 2 Points

**Pros:**
- Familiar to physics/optics users
- Compact yet informative
- Professional appearance

**Cons:**
- Subscripts might be hard to read in some fonts
- Less intuitive for non-technical users

## Proposal 3: Hierarchical Clear Text
Using full words with clear hierarchy

### Ray Paths
- ⟶ Ray Path: Primary
- ⟶ Ray Path: Reflection 1
- ⟶ Ray Path: Reflection 2
- ⟶ Ray Path: Missed

### Interaction Points
- • Hit Points: Rectangle
- • Hit Points: Circle
- • Hit Points: Lens 1
- • Hit Points: Lens 2

**Pros:**
- Very clear and explicit
- No ambiguity
- Easy to understand for all users

**Cons:**
- Takes more space
- Might be too verbose

## Proposal 4: Compact but Clear
Balancing brevity with clarity

### Ray Paths
- → Primary
- ↝ Ref 1
- ↝ Ref 2
- ✕ Missed

### Interaction Points
- • Rect Hits
- • Circ Hits
- • Lens 1 Hits
- • Lens 2 Hits

**Pros:**
- Compact
- Still readable
- Good for space-constrained UIs

**Cons:**
- Might be too terse
- Abbreviations could be unclear

## Recommendation

We recommend implementing **Proposal 1 (Descriptive with Emojis)** with some elements from Proposal 3:

```
Ray Paths:
🌟 Primary Rays
🔄 Reflection 1
🔄 Reflection 2
❌ Missed Rays

Interaction Points:
📍 Rectangle Hits
📍 Circle Hits
🎯 Lens 1 Hits
🎯 Lens 2 Hits
```

This combination provides:
- Clear visual categorization through emojis
- Explicit, unambiguous naming
- Good balance between informativeness and readability
- Friendly yet professional appearance
- Easy scanning in UI lists
- Clear distinction between different types of interactions

The emojis serve as quick visual indicators while the text provides precise information. This approach maintains professionalism while making the interface more approachable and easier to scan quickly.