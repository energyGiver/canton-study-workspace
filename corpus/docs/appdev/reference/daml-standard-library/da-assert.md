> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Assert

> Reference documentation for Daml module DA.Assert.

<span id="module-da-assert-92761" />

# DA.Assert

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

<span id="function-da-assert-asserteq-7135" />

### `assertEq`

`assertEq` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `a`, [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a`) => `a` -> `a` -> `m` ()

Check two values for equality. If they're not equal,
fail with a message.

<span id="function-da-assert-eqeqeq-18699" />

### `===`

`===` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `a`, [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a`) => `a` -> `a` -> `m` ()

Infix version of `assertEq`.

<span id="function-da-assert-assertnoteq-28771" />

### `assertNotEq`

`assertNotEq` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `a`, [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a`) => `a` -> `a` -> `m` ()

Check two values for inequality. If they're equal,
fail with a message.

<span id="function-da-assert-eqslasheq-37517" />

### `=/=`

`=/=` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `a`, [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a`) => `a` -> `a` -> `m` ()

Infix version of `assertNotEq`.

<span id="function-da-assert-assertaftermsg-14090" />

### `assertAfterMsg`

`assertAfterMsg` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`HasTime`](/appdev/reference/daml-standard-library/prelude#class-da-internal-lf-hastime-96546) `m`) => [`Text`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-text-51952) -> [`Time`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-time-63886) -> `m` ()

Check whether the given time is in the future. If it's not,
abort with a message.

<span id="function-da-assert-assertbeforemsg-56514" />

### `assertBeforeMsg`

`assertBeforeMsg` : ([`CanAssert`](/appdev/reference/daml-standard-library/prelude#class-da-internal-assert-canassert-67323) `m`, [`HasTime`](/appdev/reference/daml-standard-library/prelude#class-da-internal-lf-hastime-96546) `m`) => [`Text`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-text-51952) -> [`Time`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-time-63886) -> `m` ()

Check whether the given time is in the past. If it's not,
abort with a message.

<span id="function-da-assert-assertwithindeadline-85580" />

### `assertWithinDeadline`

`assertWithinDeadline` : [`Text`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-text-51952) -> [`Time`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-time-63886) -> [`Update`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-update-68072) ()

Check whether the ledger time of the transaction is strictly before the given deadline.
If it's not, abort with a message.

<span id="function-da-assert-assertdeadlineexceeded-21600" />

### `assertDeadlineExceeded`

`assertDeadlineExceeded` : [`Text`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-text-51952) -> [`Time`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-time-63886) -> [`Update`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-update-68072) ()

Check whether the ledger time of the transaction is at or after the given deadline.
If it's not, abort with a message.
