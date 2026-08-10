> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Logic

> Reference documentation for Daml module DA.Logic.

<span id="module-da-logic-59184" />

# DA.Logic

Logic -  Propositional calculus.

## Module Snapshot

<CardGroup cols={2}>
  <Card title="Lifecycle">
    Stable.
  </Card>

  <Card title="Notices">
    Status: `active`
    Introduced in: `3.4.9`
    Removed in: `-`
    Warnings: `0`
    Deprecations: `0`
    Deprecated since: `-`
  </Card>
</CardGroup>

## Data Types

<span id="type-da-logic-types-formula-34794" />

### `data Formula t`

A `Formula t` is a formula in propositional calculus with
propositions of type t.

Constructors:

<span id="constr-da-logic-types-proposition-6173" />

* `Proposition t`

`Proposition p` is the formula p

<span id="constr-da-logic-types-negation-48969" />

* `Negation (Formula t)`

For a formula f, `Negation f` is ¬f

<span id="constr-da-logic-types-conjunction-51637" />

* `Conjunction [Formula t]`

For formulas f1, ..., fn, `Conjunction [f1, ..., fn]` is f1 ∧ ... ∧ fn

<span id="constr-da-logic-types-disjunction-65549" />

* `Disjunction [Formula t]`

For formulas f1, ..., fn, `Disjunction [f1, ..., fn]` is f1 ∨ ... ∨ fn

Instances:

* instance [`Action`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-action-68790) [`Formula`](#type-da-logic-types-formula-34794)
* instance [`Applicative`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-applicative-9257) [`Formula`](#type-da-logic-types-formula-34794)
* instance [`Functor`](/appdev/reference/daml-standard-library/prelude#class-ghc-base-functor-31205) [`Formula`](#type-da-logic-types-formula-34794)
* instance [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `t` => [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) ([`Formula`](#type-da-logic-types-formula-34794) `t`)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `t` => [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) ([`Formula`](#type-da-logic-types-formula-34794) `t`)
* instance [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `t` => [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) ([`Formula`](#type-da-logic-types-formula-34794) `t`)

## Functions

<span id="function-da-logic-ampampamp-55265" />

### `&&&`

`&&&` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`&&&` is the ∧ operation of the boolean algebra of formulas, to
be read as "and"

<span id="function-da-logic-pipepipepipe-30747" />

### `|||`

`|||` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`|||` is the ∨ operation of the boolean algebra of formulas, to
be read as "or"

<span id="function-da-logic-true-31438" />

### `true`

`true` : [`Formula`](#type-da-logic-types-formula-34794) `t`

`true` is the 1 element of the boolean algebra of formulas,
represented as an empty conjunction.

<span id="function-da-logic-false-99028" />

### `false`

`false` : [`Formula`](#type-da-logic-types-formula-34794) `t`

`false` is the 0 element of the boolean algebra of formulas,
represented as an empty disjunction.

<span id="function-da-logic-neg-1597" />

### `neg`

`neg` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`neg` is the ¬ (negation) operation of the boolean algebra of
formulas.

<span id="function-da-logic-conj-82504" />

### `conj`

`conj` : \[[`Formula`](#type-da-logic-types-formula-34794) `t`] -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`conj` is a list version of `&&&`, enabled by the associativity
of ∧.

<span id="function-da-logic-disj-92448" />

### `disj`

`disj` : \[[`Formula`](#type-da-logic-types-formula-34794) `t`] -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`disj` is a list version of `|||`, enabled by the associativity
of ∨.

<span id="function-da-logic-frombool-36630" />

### `fromBool`

`fromBool` : [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265) -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`fromBool` converts `True` to `true` and `False` to `false`.

<span id="function-da-logic-tonnf-87354" />

### `toNNF`

`toNNF` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`toNNF` transforms a formula to negation normal form
(see [https://en.wikipedia.org/wiki/Negation\_normal\_form](https://en.wikipedia.org/wiki/Negation_normal_form)).

<span id="function-da-logic-todnf-90852" />

### `toDNF`

`toDNF` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`toDNF` turns a formula into disjunctive normal form.
(see [https://en.wikipedia.org/wiki/Disjunctive\_normal\_form](https://en.wikipedia.org/wiki/Disjunctive_normal_form)).

<span id="function-da-logic-traverse-17816" />

### `traverse`

`traverse` : [`Applicative`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-applicative-9257) `f` => (`t` -> `f` `s`) -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> `f` ([`Formula`](#type-da-logic-types-formula-34794) `s`)

An implementation of `traverse` in the usual sense.

<span id="function-da-logic-zipformulas-28999" />

### `zipFormulas`

`zipFormulas` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `s` -> [`Formula`](#type-da-logic-types-formula-34794) (`t`, `s`)

`zipFormulas` takes to formulas of same shape, meaning only
propositions are different and zips them up.

<span id="function-da-logic-substitute-65872" />

### `substitute`

`substitute` : (`t` -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`substitute` takes a truth assignment and substitutes `True` or
`False` into the respective places in a formula.

<span id="function-da-logic-reduce-40218" />

### `reduce`

`reduce` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Formula`](#type-da-logic-types-formula-34794) `t`

`reduce` reduces a formula as far as possible by:

1. Removing any occurrences of `true` and `false`;
2. Removing directly nested Conjunctions and Disjunctions;
3. Going to negation normal form.

<span id="function-da-logic-isbool-80820" />

### `isBool`

`isBool` : [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

`isBool` attempts to convert a formula to a bool. It satisfies
`isBool true == Some True` and `isBool false == Some False`.
Otherwise, it returns `None`.

<span id="function-da-logic-interpret-88386" />

### `interpret`

`interpret` : (`t` -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> [`Either`](/appdev/reference/daml-standard-library/prelude#type-da-types-either-56020) ([`Formula`](#type-da-logic-types-formula-34794) `t`) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

`interpret` is a version of `toBool` that first substitutes using
a truth function and then reduces as far as possible.

<span id="function-da-logic-substitutea-61566" />

### `substituteA`

`substituteA` : [`Applicative`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-applicative-9257) `f` => (`t` -> `f` ([`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265))) -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> `f` ([`Formula`](#type-da-logic-types-formula-34794) `t`)

`substituteA` is a version of `substitute` that allows for truth
values to be obtained from an action.

<span id="function-da-logic-interpreta-14928" />

### `interpretA`

`interpretA` : [`Applicative`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-applicative-9257) `f` => (`t` -> `f` ([`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265))) -> [`Formula`](#type-da-logic-types-formula-34794) `t` -> `f` ([`Either`](/appdev/reference/daml-standard-library/prelude#type-da-types-either-56020) ([`Formula`](#type-da-logic-types-formula-34794) `t`) [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265))

`interpretA` is a version of `interpret` that allows for truth
values to be obtained form an action.

## Orphan Typeclass Instances

* instance [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `t` => [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) ([`Formula`](#type-da-logic-types-formula-34794) `t`)

* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `t` => [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) ([`Formula`](#type-da-logic-types-formula-34794) `t`)

* instance [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `t` => [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) ([`Formula`](#type-da-logic-types-formula-34794) `t`)

* instance [`Functor`](/appdev/reference/daml-standard-library/prelude#class-ghc-base-functor-31205) [`Formula`](#type-da-logic-types-formula-34794)

* instance [`Applicative`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-applicative-9257) [`Formula`](#type-da-logic-types-formula-34794)

* instance [`Action`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-action-68790) [`Formula`](#type-da-logic-types-formula-34794)
