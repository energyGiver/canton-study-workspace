> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Math

> Reference documentation for Daml module DA.Math.

<span id="module-da-math-30023" />

# DA.Math

Math - Utility Math functions for `Decimal`

The this library is designed to give good precision, typically giving 9 correct decimal places.

The numerical algorithms run with many iterations to achieve that precision and are interpreted

by the Daml runtime so they are not performant. Their use is not advised in performance critical

contexts.

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

## Functions

<span id="function-da-math-starstar-89123" />

### `**`

`**` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

Take a power of a number Example: `2.0 ** 3.0 == 8.0`.

<span id="function-da-math-sqrt-24467" />

### `sqrt`

`sqrt` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

Calculate the square root of a Decimal.

```
>>> sqrt 1.44
1.2
```

<span id="function-da-math-exp-84235" />

### `exp`

`exp` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

The exponential function. Example: `exp 0.0 == 1.0`

<span id="function-da-math-log-52192" />

### `log`

`log` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

The natural logarithm. Example: `log 10.0 == 2.30258509299`

<span id="function-da-math-logbase-64267" />

### `logBase`

`logBase` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

The logarithm of a number to a given base. Example: `log 10.0 100.0 == 2.0`

<span id="function-da-math-sin-61636" />

### `sin`

`sin` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

`sin` is the sine function

<span id="function-da-math-cos-82859" />

### `cos`

`cos` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

`cos` is the cosine function

<span id="function-da-math-tan-54959" />

### `tan`

`tan` : [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135) -> [`Decimal`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-decimal-18135)

`tan` is the tangent function
