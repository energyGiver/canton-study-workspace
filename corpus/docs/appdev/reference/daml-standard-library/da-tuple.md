> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Tuple

> Reference documentation for Daml module DA.Tuple.

<span id="module-da-tuple-81988" />

# DA.Tuple

Tuple - Ubiquitous functions of tuples.

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

<span id="function-da-tuple-first-48871" />

### `first`

`first` : (`a` -> `a'`) -> (`a`, `b`) -> (`a'`, `b`)

The pair obtained from a pair by application of a programmer
supplied function to the argument pair's first field.

<span id="function-da-tuple-second-48360" />

### `second`

`second` : (`b` -> `b'`) -> (`a`, `b`) -> (`a`, `b'`)

The pair obtained from a pair by application of a programmer
supplied function to the argument pair's second field.

<span id="function-da-tuple-both-63511" />

### `both`

`both` : (`a` -> `b`) -> (`a`, `a`) -> (`b`, `b`)

The pair obtained from a pair by application of a programmer
supplied function to both the argument pair's first and second
fields.

<span id="function-da-tuple-swap-76115" />

### `swap`

`swap` : (`a`, `b`) -> (`b`, `a`)

The pair obtained from a pair by permuting the order of the
argument pair's first and second fields.

<span id="function-da-tuple-dupe-14430" />

### `dupe`

`dupe` : `a` -> (`a`, `a`)

Duplicate a single value into a pair.

> dupe 12 == (12, 12)

<span id="function-da-tuple-fst3-84676" />

### `fst3`

`fst3` : (`a`, `b`, `c`) -> `a`

Extract the 'fst' of a triple.

<span id="function-da-tuple-snd3-63950" />

### `snd3`

`snd3` : (`a`, `b`, `c`) -> `b`

Extract the 'snd' of a triple.

<span id="function-da-tuple-thd3-58697" />

### `thd3`

`thd3` : (`a`, `b`, `c`) -> `c`

Extract the final element of a triple.

<span id="function-da-tuple-curry3-2900" />

### `curry3`

`curry3` : ((`a`, `b`, `c`) -> `d`) -> `a` -> `b` -> `c` -> `d`

Converts an uncurried function to a curried function.

<span id="function-da-tuple-uncurry3-51859" />

### `uncurry3`

`uncurry3` : (`a` -> `b` -> `c` -> `d`) -> (`a`, `b`, `c`) -> `d`

Converts a curried function to a function on a triple.
