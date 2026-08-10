> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.ContractKeys

> Reference documentation for Daml module DA.ContractKeys.

<span id="module-da-contractkeys-19667" />

# DA.ContractKeys

Note: Docs TODO ([https://github.com/digital-asset/daml/issues/22673](https://github.com/digital-asset/daml/issues/22673))

## Module Snapshot

<CardGroup cols={2}>
  <Card title="Lifecycle">
    Stable.
  </Card>

  <Card title="Notices">
    Status: `active`
    Introduced in: `3.5.1`
    Removed in: `-`
    Warnings: `0`
    Deprecations: `0`
    Deprecated since: `-`
  </Card>
</CardGroup>

## Functions

<span id="function-da-internal-template-functions-lookupnbykey-93090" />

### `lookupNByKey`

`lookupNByKey` : [`HasLookupNByKey`](/appdev/reference/daml-standard-library/prelude#class-da-internal-template-functions-haslookupnbykey-35508) `t` `k` => [`Int`](/appdev/reference/daml-standard-library/prelude#type-ghc-types-int-37261) -> `k` -> [`Update`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-update-68072) \[([`ContractId`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-contractid-95282) `t`, `t`)]

Look up up to n contracts associated with the passed key. Contracts created
within a transaction are returned first (in recency order), then disclosed
contracts, then nonlocal contracts.

You must pass the `t` using an explicit type application. For instance, if
you want to query 3 contracts of template `Account` given by its key `k`, you
must call \`lookupNByKey @Account 3 k.

<span id="function-da-internal-template-functions-lookupallbykey-2641" />

### `lookupAllByKey`

`lookupAllByKey` : [`HasLookupNByKey`](/appdev/reference/daml-standard-library/prelude#class-da-internal-template-functions-haslookupnbykey-35508) `t` `k` => `k` -> [`Update`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-update-68072) \[([`ContractId`](/appdev/reference/daml-standard-library/prelude#type-da-internal-lf-contractid-95282) `t`, `t`)]

Shorthand for `lookupNByKey` with n larger than the amount of contracts that
can exist for a key (1000000), therefore returning all contracts
