> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# DA.Internal.Interface.AnyView.Types

> Reference documentation for Daml module DA.Internal.Interface.AnyView.Types.

<span id="module-da-internal-interface-anyview-types-13315" />

# DA.Internal.Interface.AnyView\.Types

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

<span id="type-da-internal-interface-anyview-types-anyview-16883" />

### `data AnyView`

Existential contract key type that can wrap an arbitrary contract key.

Constructors:

<span id="constr-da-internal-interface-anyview-types-anyview-58868" />

* `AnyView`

<ResponseField name="getAnyView" type="Any" />

<ResponseField name="getAnyViewInterfaceTypeRep" type="InterfaceTypeRep" />

Instances:

* instance [`GetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-getfield-53979) `getAnyView` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) `Any`
* instance [`GetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-getfield-53979) `getAnyViewInterfaceTypeRep` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)
* instance [`SetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-setfield-4311) `getAnyView` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) `Any`
* instance [`SetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-setfield-4311) `getAnyViewInterfaceTypeRep` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)

<span id="type-da-internal-interface-anyview-types-interfacetyperep-5047" />

### `data InterfaceTypeRep`

Constructors:

<span id="constr-da-internal-interface-anyview-types-interfacetyperep-24802" />

* `InterfaceTypeRep`

<ResponseField name="getInterfaceTypeRep" type="TypeRep" />

Instances:

* instance [`GetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-getfield-53979) `getAnyViewInterfaceTypeRep` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)
* instance [`SetField`](/appdev/reference/daml-standard-library/da-record#class-da-internal-record-setfield-4311) `getAnyViewInterfaceTypeRep` [`AnyView`](#type-da-internal-interface-anyview-types-anyview-16883) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)
* instance [`Eq`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-eq-22713) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)
* instance [`Ord`](/appdev/reference/daml-standard-library/prelude#class-ghc-classes-ord-6395) [`InterfaceTypeRep`](#type-da-internal-interface-anyview-types-interfacetyperep-5047)
