# Reasoning Engine

## Purpose

The reasoning layer provides deterministic, inspectable evaluation on top of authored evidence, constraints, and scenarios.

## Early-phase scope

The MVP reasoning contract is intentionally narrow:

- check scenario compatibility against visible claims and constraints
- surface contradictions and tensions
- track assumption load
- report unresolved explanatory gaps
- emit a compatibility band with visible contributing factors

## Explicit non-goals

- no posterior probability claims
- no black-box scoring
- no autonomous scenario search
- no optimizer loops

## Compatibility factors

Early compatibility reports should surface:

- supporting claims
- contradicting claims
- hard constraint failures
- soft constraint tensions
- unresolved gaps
- assumption load

The final output is a compatibility band, not a winner selection.
