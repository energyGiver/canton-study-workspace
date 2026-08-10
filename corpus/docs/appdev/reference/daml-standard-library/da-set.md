> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Set

> Reference documentation for Daml module DA.Set.

<span id="module-da-set-6124" />

# DA.Set

Note: This is only supported in Daml-LF 1.11 or later.

This module exports the generic set type `Set k` and associated

functions. This module should be imported qualified, for example:

```

import DA.Set (Set)

import DA.Set qualified as S

```

This will give access to the `Set` type, and the various operations

as `S.lookup`, `S.insert`, `S.fromList`, etc.

`Set k` internally uses the built-in order for the type `k`.

This means that keys that contain functions are not comparable

and will result in runtime errors. To prevent this, the `Ord k`

instance is required for most set operations. It is recommended to

only use `Set k` for key types that have an `Ord k` instance

that is derived automatically using `deriving`:

```

data K = ...

deriving (Eq, Ord)

```

This includes all built-in types that aren't function types, such as

`Int`, `Text`, `Bool`, `(a, b)` assuming `a` and `b` have default

`Ord` instances, `Optional t` and `[t]` assuming `t` has a

default `Ord` instance, `Map k v` assuming `k` and `v` have

default `Ord` instances, and `Set k` assuming `k` has a

default `Ord` instance.

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

<span id="type-da-set-types-set-90436" />

### `data Set k`

The type of a set. This is a wrapper over the `Map` type.

Constructors:

<span id="constr-da-set-types-set-78105" />

* `Set`

<ResponseField name="map" type="Map k ()" />

Instances:

* instance [`Foldable`](/appdev/reference/daml-standard-library/da-foldable#class-da-foldable-foldable-25994) [`Set`](#type-da-set-types-set-90436)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Monoid`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-monoid-6742) ([`Set`](#type-da-set-types-set-90436) `k`)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Semigroup`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-semigroup-78998) ([`Set`](#type-da-set-types-set-90436) `k`)
* instance [`GetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-getfield-53979) `map` ([`Set`](#type-da-set-types-set-90436) `k`) ([`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` ())
* instance [`SetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-setfield-4311) `map` ([`Set`](#type-da-set-types-set-90436) `k`) ([`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` ())
* instance [`IsParties`](/appdev/reference/daml-standard-library/prelude#class-da-internal-template-functions-isparties-53750) ([`Set`](#type-da-set-types-set-90436) [`Party`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-party-57932))
* instance `Serializable` `k` => `Serializable` ([`Set`](#type-da-set-types-set-90436) `k`)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) ([`Set`](#type-da-set-types-set-90436) `k`)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) ([`Set`](#type-da-set-types-set-90436) `k`)
* instance ([`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `k`) => [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) ([`Set`](#type-da-set-types-set-90436) `k`)

## Functions

<span id="function-da-set-empty-19742" />

### `empty`

`empty` : [`Set`](#type-da-set-types-set-90436) `k`

The empty set.

<span id="function-da-set-size-6437" />

### `size`

`size` : [`Set`](#type-da-set-types-set-90436) `k` -> [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261)

The number of elements in the set.

<span id="function-da-set-tolist-26355" />

### `toList`

`toList` : [`Set`](#type-da-set-types-set-90436) `k` -> \[`k`]

Convert the set to a list of elements.

<span id="function-da-set-fromlist-9190" />

### `fromList`

`fromList` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => \[`k`] -> [`Set`](#type-da-set-types-set-90436) `k`

Create a set from a list of elements.

<span id="function-da-set-tomap-37614" />

### `toMap`

`toMap` : [`Set`](#type-da-set-types-set-90436) `k` -> [`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` ()

Convert a `Set` into a `Map`.

<span id="function-da-set-frommap-15501" />

### `fromMap`

`fromMap` : [`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` () -> [`Set`](#type-da-set-types-set-90436) `k`

Create a `Set` from a `Map`.

<span id="function-da-set-member-75542" />

### `member`

`member` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

Is the element in the set?

<span id="function-da-set-notmember-79044" />

### `notMember`

`notMember` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

Is the element not in the set?
`notMember k s` is equivalent to `not (member k s)`.

<span id="function-da-set-null-99389" />

### `null`

`null` : [`Set`](#type-da-set-types-set-90436) `k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

Is this the empty set?

<span id="function-da-set-insert-58479" />

### `insert`

`insert` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

Insert an element in a set. If the set already contains the
element, this returns the set unchanged.

<span id="function-da-set-filter-76182" />

### `filter`

`filter` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

Filter all elements that satisfy the predicate.

<span id="function-da-set-delete-52281" />

### `delete`

`delete` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

Delete an element from a set.

<span id="function-da-set-singleton-15574" />

### `singleton`

`singleton` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => `k` -> [`Set`](#type-da-set-types-set-90436) `k`

Create a singleton set.

<span id="function-da-set-union-79876" />

### `union`

`union` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

The union of two sets.

<span id="function-da-set-intersection-70017" />

### `intersection`

`intersection` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

The intersection of two sets.

<span id="function-da-set-difference-68545" />

### `difference`

`difference` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k`

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
`difference x y` returns the set consisting of all
elements in `x` that are not in `y`.

>>> fromList [1, 2, 3] `difference` fromList [1, 4]
fromList [2, 3]
```

<span id="function-da-set-issubsetof-34493" />

### `isSubsetOf`

`isSubsetOf` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

`isSubsetOf a b` returns true if `a` is a subset of `b`,
that is, if every element of `a` is in `b`.

<span id="function-da-set-ispropersubsetof-90093" />

### `isProperSubsetOf`

`isProperSubsetOf` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Set`](#type-da-set-types-set-90436) `k` -> [`Set`](#type-da-set-types-set-90436) `k` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

`isProperSubsetOf a b` returns true if `a` is a proper subset of `b`.
That is, if `a` is a subset of `b` but not equal to `b`.

## Orphan Typeclass Instances

* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) ([`Set`](#type-da-set-types-set-90436) `k`)

* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) ([`Set`](#type-da-set-types-set-90436) `k`)

* instance ([`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k`, [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) `k`) => [`Show`](/appdev/reference/daml-standard-library/prelude#class-ghc-show-show-65360) ([`Set`](#type-da-set-types-set-90436) `k`)

* instance [`IsParties`](/appdev/reference/daml-standard-library/prelude#class-da-internal-template-functions-isparties-53750) ([`Set`](#type-da-set-types-set-90436) [`Party`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-party-57932))

* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Semigroup`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-semigroup-78998) ([`Set`](#type-da-set-types-set-90436) `k`)

* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => [`Monoid`](/appdev/reference/daml-standard-library/prelude#class-da-internal-prelude-monoid-6742) ([`Set`](#type-da-set-types-set-90436) `k`)

* instance [`GetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-getfield-53979) `map` ([`Set`](#type-da-set-types-set-90436) `k`) ([`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` ())

* instance [`SetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-setfield-4311) `map` ([`Set`](#type-da-set-types-set-90436) `k`) ([`Map`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-map-90052) `k` ())

* instance [`Foldable`](/appdev/reference/daml-standard-library/da-foldable#class-da-foldable-foldable-25994) [`Set`](#type-da-set-types-set-90436)
