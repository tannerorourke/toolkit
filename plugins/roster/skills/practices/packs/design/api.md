# API

How a library designer decides the names, defaults, errors, and first example a developer meets in a public interface.

Read this when you design a unit of the `api` medium: a library, CLI, or service interface a developer calls.

## What the unit decides

Names, defaults, and errors; the first five minutes of use; the documented example.

## Rules

1. Give every object the same small set of methods. Consistency lets a developer carry what they learned from one object to the next (scikit-learn API design, Buitinck et al.: https://ar5iv.labs.arxiv.org/html/1309.0238).
2. Expose parameters and learned or computed values as public attributes, so a developer can inspect state (scikit-learn paper).
3. Add a custom class only for the main concepts. Represent everything else with plain, existing types (scikit-learn paper).
4. Make parts compose: the output of one should be a valid input to another (scikit-learn paper).
5. Define a sensible default for every parameter a caller would otherwise have to choose (scikit-learn paper).
6. Make errors meaningful and well-behaved. Document the error, panic, and safety conditions of every function (Rust API Guidelines, C-GOOD-ERR and C-FAILURE: https://rust-lang.github.io/api-guidelines/checklist.html).
7. Let arguments carry meaning through types, never through a bare `bool` or an optional (Rust API Guidelines, C-CUSTOM-TYPE).
8. Give every public item a runnable example (Rust API Guidelines, C-EXAMPLE).
9. Model the interface as resources with standard methods, and prefer those over custom ones. Number and cite each design decision (Google API Improvement Proposals, AIP-121: https://google.aip.dev/).
10. Design for the newcomer's learnability and the expert's efficiency and correctness. Check the interface with think-aloud sessions or a heuristic review (Myers and Stylos, "Improving API Usability", CACM 2016: https://cacmb4.acm.org/magazines/2016/6/202645-improving-api-usability).
11. Write each rule as something a reviewer can check from the interface and its docs alone. The Rust checklist works this way: 54 items in 11 sections, each checkable.

## Files

Under `<unit>/` in the design folder; an `api` unit has no `sample.md`, because the documented example lives in `handoff.md`:

- `handoff.md`: the names and signatures; the default for each parameter; the error list with condition and fix per error; the documented example a developer runs in the first five minutes, with its expected output.
- `review.md`: the user's reactions and approval line, in the shape the core gives.

## Pass condition

Every public item has a name, a default or a stated reason for none, an error list, and one runnable example, and the first-five-minutes example runs as written.
