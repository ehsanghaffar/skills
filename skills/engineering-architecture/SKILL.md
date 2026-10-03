---
name: engineering-architecture
description: Apply persistent engineering and architectural principles to every task. Use this skill whenever you are about to make changes to a codebase, design a new feature, or perform a code review to ensure architectural integrity and quality.
---

# Engineering & Architecture Memory

These are persistent operating principles. Apply them to every task unless the current task explicitly overrides them.

## 1. Think Beyond the Task
Do not treat a task as isolated code generation.

Before making changes, understand:

- the existing architecture
- relevant boundaries and dependencies
- established patterns and conventions
- quality attributes and non-functional requirements
- constraints and trade-offs
- likely architectural impact of the change
Prefer improving the system as a whole over producing locally correct but architecturally harmful code.

## 2. Audit Before Changing
When working in an existing codebase:

- inspect the relevant implementation first
- identify existing abstractions and patterns before introducing new ones
- look for architectural smells, unnecessary coupling, duplication, boundary violations, and inconsistent patterns
- distinguish real problems from merely different preferences
Do not rewrite or redesign working architecture without evidence that it is necessary.

## 3. Requirements Include Quality Attributes
Do not optimize only for functional correctness.

Consider relevant quality attributes such as:

- maintainability
- reliability
- security
- performance
- scalability
- observability
- testability
- portability
- simplicity
When these attributes matter, make them explicit in implementation and verification.

## 4. Respect Boundaries
Treat architectural boundaries as first-class constraints.

Do not introduce:

- forbidden dependencies
- layer violations
- cross-domain state access
- accidental coupling
- duplicated ownership of business logic
- shortcuts that bypass established interfaces
Prefer explicit, stable interfaces between components.

## 5. Prefer Constraints Over Prescriptions
When solving a problem, reason from:

- desired outcome
- constraints
- quality requirements
- acceptance criteria
Do not blindly follow an imagined implementation.

Choose the simplest design that satisfies the requirements and constraints.

## 6. Minimize Architectural Complexity
Do not over-engineer.

Prefer:

- the smallest viable architecture
- the smallest useful abstraction
- existing infrastructure over new infrastructure
- simple solutions over speculative flexibility
Introduce additional layers, services, abstractions, or dependencies only when they solve a demonstrated problem.

## 7. Verify Architecture With Evidence
Do not assume that an architecture is good because it looks good.

Whenever practical, verify important architectural properties through:

- tests
- static analysis
- type checks
- dependency checks
- performance measurements
- security checks
- integration tests
- architecture-specific assertions
Prefer measurable evidence over subjective confidence.

## 8. Treat Agents as Reviewers, Not Only Implementers
While implementing a task, actively inspect for:

- architectural flaws
- security vulnerabilities
- unnecessary complexity
- inconsistent patterns
- technical debt introduced by the change
- violations of project conventions
Surface meaningful issues even when they are outside the immediate task, but do not expand scope unnecessarily.

## 9. Separate Facts From Preferences
Do not label something as an architectural problem merely because it is different from your preferred style.

Distinguish between:

- actual defects
- measurable risks
- maintainability concerns
- architectural violations
- reasonable alternative designs
- personal preferences
Only recommend changes when there is a concrete engineering reason.

## 10. Security Is an Architectural Concern
Consider security at the architecture and implementation levels.

Check relevant:

- trust boundaries
- authentication and authorization
- input validation
- data exposure
- secrets handling
- SSRF and injection risks
- unsafe external integrations
- privilege escalation paths
Never assume security is someone else's responsibility.

## 11. Preserve Existing Behavior
Unless a change explicitly requires otherwise:

- preserve public behavior
- preserve valid existing APIs
- avoid unnecessary migrations
- avoid unrelated refactors
- maintain backward compatibility where required
Every architectural change should have a clear reason and controlled blast radius.

## 12. Make Trade-offs Explicit
When multiple viable designs exist, reason about the trade-offs.

Consider:

- complexity
- operational cost
- performance
- reliability
- maintainability
- scalability
- developer experience
Do not optimize one dimension while silently degrading important others.

## 13. Use the Smallest Proof
For uncertain architectural decisions, prefer a small experiment, prototype, benchmark, or focused test that can validate the assumption before committing to a large implementation.

Reduce uncertainty with evidence before increasing complexity.

## 14. Definition of Done
A task is not complete merely because the code compiles.

When relevant, completion should include:

- implementation
- appropriate tests
- validation of important architectural constraints
- verification of quality attributes
- review for unintended side effects
- documentation when the architectural decision is non-obvious

## Core Principle
Optimize for:

**Correctness + Simplicity + Architectural Integrity + Measurable Evidence**

not merely:

**"The requested feature works."**
