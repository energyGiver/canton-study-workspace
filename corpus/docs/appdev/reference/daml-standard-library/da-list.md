> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.List

> Reference documentation for Daml module DA.List.

<span id="module-da-list-85985" />

# DA.List

List

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

<span id="function-da-list-sort-96399" />

### `sort`

`sort` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `a` => \[`a`] -> \[`a`]

The `sort` function implements a stable sorting algorithm. It is
a special case of `sortBy`, which allows the programmer to supply
their own comparison function.

Elements are arranged from lowest to highest, keeping duplicates in
the order they appeared in the input (a stable sort).

<span id="function-da-list-sortby-71202" />

### `sortBy`

`sortBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> \[`a`]

The `sortBy` function is the non-overloaded version of `sort`.

<span id="function-da-list-minimumby-84625" />

### `minimumBy`

`minimumBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> `a`

`minimumBy f xs` returns the first element `x` of `xs` for which `f x y`
is either `LT` or `EQ` for all other `y` in `xs`. `xs` must be non-empty.

<span id="function-da-list-maximumby-22187" />

### `maximumBy`

`maximumBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> `a`

`maximumBy f xs` returns the first element `x` of `xs` for which `f x y`
is either `GT` or `EQ` for all other `y` in `xs`. `xs` must be non-empty.

<span id="function-da-list-sorton-99758" />

### `sortOn`

`sortOn` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`a` -> `k`) -> \[`a`] -> \[`a`]

Sort a list by comparing the results of a key function applied to
each element. `sortOn f` is equivalent to `sortBy (comparing f)`,
but has the performance advantage of only evaluating `f` once for
each element in the input list. This is sometimes called the
decorate-sort-undecorate paradigm.

Elements are arranged from from lowest to highest, keeping
duplicates in the order they appeared in the input.

<span id="function-da-list-minimumon-90785" />

### `minimumOn`

`minimumOn` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`a` -> `k`) -> \[`a`] -> `a`

`minimumOn f xs` returns the first element `x` of `xs` for which `f x`
is smaller than or equal to any other `f y` for `y` in `xs`. `xs` must be
non-empty.

<span id="function-da-list-maximumon-98335" />

### `maximumOn`

`maximumOn` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`a` -> `k`) -> \[`a`] -> `a`

`maximumOn f xs` returns the first element `x` of `xs` for which `f x`
is greater than or equal to any other `f y` for `y` in `xs`. `xs` must be
non-empty.

<span id="function-da-list-mergeby-31951" />

### `mergeBy`

`mergeBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> \[`a`] -> \[`a`]

Merge two sorted lists using into a single, sorted whole, allowing
the programmer to specify the comparison function.

<span id="function-da-list-combinepairs-8661" />

### `combinePairs`

`combinePairs` : (`a` -> `a` -> `a`) -> \[`a`] -> \[`a`]

Combine elements pairwise by means of a programmer supplied
function from two list inputs into a single list.

<span id="function-da-list-foldbalanced1-46720" />

### `foldBalanced1`

`foldBalanced1` : (`a` -> `a` -> `a`) -> \[`a`] -> `a`

Fold a non-empty list in a balanced way. Balanced means that each
element has approximately the same depth in the operator
tree. Approximately the same depth means that the difference
between maximum and minimum depth is at most 1. The accumulation
operation must be associative and commutative in order to get the
same result as `foldl1` or `foldr1`.

<span id="function-da-list-group-62411" />

### `group`

`group` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[\[`a`]]

The 'group' function groups equal elements into sublists such
that the concatenation of the result is equal to the argument.

<span id="function-da-list-groupby-62666" />

### `groupBy`

`groupBy` : (`a` -> `a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> \[\[`a`]]

The 'groupBy' function is the non-overloaded version of 'group'.

<span id="function-da-list-groupon-4918" />

### `groupOn`

`groupOn` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `k` => (`a` -> `k`) -> \[`a`] -> \[\[`a`]]

Similar to 'group', except that the equality is done on an
extracted value.

<span id="function-da-list-dedup-27230" />

### `dedup`

`dedup` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `a` => \[`a`] -> \[`a`]

`dedup l` removes duplicate elements from a list. In particular,
it keeps only the first occurrence of each element. It is a
special case of `dedupBy`, which allows the programmer to supply
their own equality test.
`dedup` is called `nub` in Haskell.

<span id="function-da-list-dedupby-29335" />

### `dedupBy`

`dedupBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> \[`a`]

A version of `dedup` with a custom predicate.

<span id="function-da-list-dedupon-81495" />

### `dedupOn`

`dedupOn` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`a` -> `k`) -> \[`a`] -> \[`a`]

A version of `dedup` where deduplication is done
after applyng function. Example use: `dedupOn (.employeeNo) employees`

<span id="function-da-list-dedupsort-78698" />

### `dedupSort`

`dedupSort` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `a` => \[`a`] -> \[`a`]

The `dedupSort` function sorts and removes duplicate elements from a
list. In particular, it keeps only the first occurrence of each
element.

<span id="function-da-list-dedupsortby-97595" />

### `dedupSortBy`

`dedupSortBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> \[`a`]

A version of `dedupSort` with a custom predicate.

<span id="function-da-list-unique-23008" />

### `unique`

`unique` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `a` => \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

Returns True if and only if there are no duplicate elements in the given list.

<span id="function-da-list-uniqueby-86149" />

### `uniqueBy`

`uniqueBy` : (`a` -> `a` -> [`Ordering`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-ordering-35353)) -> \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

A version of `unique` with a custom predicate.

<span id="function-da-list-uniqueon-39349" />

### `uniqueOn`

`uniqueOn` : [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) `k` => (`a` -> `k`) -> \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

Returns True if and only if there are no duplicate elements in the given list
after applyng function. Example use: `assert $ uniqueOn (.employeeNo) employees`

<span id="function-da-list-replace-72492" />

### `replace`

`replace` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> \[`a`] -> \[`a`]

Given a list and a replacement list, replaces each occurance of
the search list with the replacement list in the operation list.

<span id="function-da-list-dropprefix-26566" />

### `dropPrefix`

`dropPrefix` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> \[`a`]

Drops the given prefix from a list. It returns the original
sequence if the sequence doesn't start with the given prefix.

<span id="function-da-list-dropsuffix-41813" />

### `dropSuffix`

`dropSuffix` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> \[`a`]

Drops the given suffix from a list. It returns the original
sequence if the sequence doesn't end with the given suffix.

<span id="function-da-list-stripprefix-65866" />

### `stripPrefix`

`stripPrefix` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) \[`a`]

The `stripPrefix` function drops the given prefix from a list.
It returns `None` if the list did not start with the prefix
given, or `Some` the list after the prefix, if it does.

<span id="function-da-list-stripsuffix-23153" />

### `stripSuffix`

`stripSuffix` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) \[`a`]

Return the prefix of the second list if its suffix matches the
entire first list.

<span id="function-da-list-stripinfix-68205" />

### `stripInfix`

`stripInfix` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) (\[`a`], \[`a`])

Return the string before and after the search string or `None`
if the search string is not found.

```
>>> stripInfix [0,0] [1,0,0,2,0,0,3]
Some ([1], [2,0,0,3])

>>> stripInfix [0,0] [1,2,0,4,5]
None
```

<span id="function-da-list-isprefixof-27346" />

### `isPrefixOf`

`isPrefixOf` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

The `isPrefixOf` function takes two lists and returns `True` if
and only if the first is a prefix of the second.

<span id="function-da-list-issuffixof-26645" />

### `isSuffixOf`

`isSuffixOf` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

The `isSuffixOf` function takes two lists and returns `True` if
and only if the first list is a suffix of the second.

<span id="function-da-list-isinfixof-7159" />

### `isInfixOf`

`isInfixOf` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)

The `isInfixOf` function takes two lists and returns `True` if
and only if the first list is contained anywhere within the second.

<span id="function-da-list-mapaccuml-18387" />

### `mapAccumL`

`mapAccumL` : (`acc` -> `x` -> (`acc`, `y`)) -> `acc` -> \[`x`] -> (`acc`, \[`y`])

The `mapAccumL` function combines the behaviours of `map` and
`foldl`; it applies a function to each element of a list, passing
an accumulating parameter from left to right, and returning a final
value of this accumulator together with the new list.

<span id="function-da-list-mapwithindex-75685" />

### `mapWithIndex`

`mapWithIndex` : ([`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261) -> `a` -> `b`) -> \[`a`] -> \[`b`]

A generalisation of `map`, `mapWithIndex` takes a mapping
function that also depends on the element's index, and applies it to every
element in the sequence.

<span id="function-da-list-inits-75071" />

### `inits`

`inits` : \[`a`] -> \[\[`a`]]

The `inits` function returns all initial segments of the argument,
shortest first.

<span id="function-da-list-intersperse-31314" />

### `intersperse`

`intersperse` : `a` -> \[`a`] -> \[`a`]

The `intersperse` function takes an element and a list and
"intersperses" that element between the elements of the list.

<span id="function-da-list-intercalate-85238" />

### `intercalate`

`intercalate` : \[`a`] -> \[\[`a`]] -> \[`a`]

`intercalate` inserts the list `xs` in between the lists in `xss`
and concatenates the result.

<span id="function-da-list-tails-57647" />

### `tails`

`tails` : \[`a`] -> \[\[`a`]]

The `tails` function returns all final segments of the argument,
longest first.

<span id="function-da-list-dropwhileend-92606" />

### `dropWhileEnd`

`dropWhileEnd` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> \[`a`]

A version of `dropWhile` operating from the end.

<span id="function-da-list-takewhileend-40268" />

### `takeWhileEnd`

`takeWhileEnd` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> \[`a`]

A version of `takeWhile` operating from the end.

<span id="function-da-list-transpose-84171" />

### `transpose`

`transpose` : \[\[`a`]] -> \[\[`a`]]

The `transpose` function transposes the rows and columns of its
argument.

<span id="function-da-list-breakend-41551" />

### `breakEnd`

`breakEnd` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> (\[`a`], \[`a`])

Break, but from the end.

<span id="function-da-list-breakon-39026" />

### `breakOn`

`breakOn` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> (\[`a`], \[`a`])

Find the first instance of `needle` in `haystack`.
The first element of the returned tuple is the prefix of `haystack`
before `needle` is matched. The second is the remainder of
`haystack`, starting with the match.  If you want the remainder
*without* the match, use `stripInfix`.

<span id="function-da-list-breakonend-30980" />

### `breakOnEnd`

`breakOnEnd` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> (\[`a`], \[`a`])

Similar to `breakOn`, but searches from the end of the
string.

The first element of the returned tuple is the prefix of `haystack`
up to and including the last match of `needle`.  The second is the
remainder of `haystack`, following the match.

<span id="function-da-list-linesby-68954" />

### `linesBy`

`linesBy` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> \[\[`a`]]

A variant of `lines` with a custom test. In particular, if there
is a trailing separator it will be discarded.

<span id="function-da-list-wordsby-74460" />

### `wordsBy`

`wordsBy` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> \[\[`a`]]

A variant of `words` with a custom test. In particular, adjacent
separators are discarded, as are leading or trailing separators.

<span id="function-da-list-head-92101" />

### `head`

`head` : \[`a`] -> `a`

Extract the first element of a list, which must be non-empty.

<span id="function-da-list-tail-16805" />

### `tail`

`tail` : \[`a`] -> \[`a`]

Extract the elements after the head of a list, which must be
non-empty.

<span id="function-da-list-last-56071" />

### `last`

`last` : \[`a`] -> `a`

Extract the last element of a list, which must be finite and
non-empty.

<span id="function-da-list-init-2389" />

### `init`

`init` : \[`a`] -> \[`a`]

Return all the elements of a list except the last one. The list
must be non-empty.

<span id="function-da-list-foldl1-60813" />

### `foldl1`

`foldl1` : (`a` -> `a` -> `a`) -> \[`a`] -> `a`

Left associative fold of a list that must be non-empty.

<span id="function-da-list-foldr1-23463" />

### `foldr1`

`foldr1` : (`a` -> `a` -> `a`) -> \[`a`] -> `a`

Right associative fold of a list that must be non-empty.

<span id="function-da-list-repeatedly-9930" />

### `repeatedly`

`repeatedly` : (\[`a`] -> (`b`, \[`a`])) -> \[`a`] -> \[`b`]

Apply some operation repeatedly, producing an element of output
and the remainder of the list.

<span id="function-da-list-chunksof-64138" />

### `chunksOf`

`chunksOf` : [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261) -> \[`a`] -> \[\[`a`]]

Splits a list into chunks of length @n\@.
@n@ must be strictly greater than zero.
The last chunk will be shorter than @n@ in case the length of the input is
not divisible by @n\@.

<span id="function-da-list-delete-22340" />

### `delete`

`delete` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => `a` -> \[`a`] -> \[`a`]

`delete x` removes the first occurrence of `x` from its list argument.
For example,

```
> delete "a" ["b","a","n","a","n","a"]
["b","n","a","n","a"]
```

It is a special case of 'deleteBy', which allows the programmer to
supply their own equality test.

<span id="function-da-list-deleteby-50465" />

### `deleteBy`

`deleteBy` : (`a` -> `a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> `a` -> \[`a`] -> \[`a`]

The 'deleteBy' function behaves like 'delete', but takes a
user-supplied equality predicate.

```
> deleteBy (<=) 4 [1..10]
[1,2,3,5,6,7,8,9,10]
```

<span id="function-da-list-x-54181" />

### `\\`

`\\` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => \[`a`] -> \[`a`] -> \[`a`]

The `\\` function is list difference (non-associative).
In the result of `xs \\ ys`, the first occurrence of each element of
`ys` in turn (if any) has been removed from `xs`.  Thus

```
(xs ++ ys) \\ xs == ys
```

Note this function is *O(n\*m)* given lists of size *n* and *m*.

<span id="function-da-list-singleton-17649" />

### `singleton`

`singleton` : `a` -> \[`a`]

Produce a singleton list.

```
>>> singleton True
[True]
```

<span id="function-da-list-bangbang-90127" />

### `!!`

`!!` : \[`a`] -> [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261) -> `a`

List index (subscript) operator, starting from 0.
For example, `xs !! 2` returns the third element in `xs`.
Raises an error if the index is not suitable for the given list.
The function has complexity *O(n)* where *n* is the index given,
unlike in languages such as Java where array indexing is *O(1)*.

<span id="function-da-list-elemindex-4965" />

### `elemIndex`

`elemIndex` : [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) `a` => `a` -> \[`a`] -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261)

Find index of element in given list.
Will return `None` if not found.

<span id="function-da-list-findindex-82181" />

### `findIndex`

`findIndex` : (`a` -> [`Bool`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-bool-66265)) -> \[`a`] -> [`Optional`](/appdev/reference/daml-standard-library/prelude#type-da-internal-prelude-optional-37153) [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261)

Find index, given predicate, of first matching element.
Will return `None` if not found.
