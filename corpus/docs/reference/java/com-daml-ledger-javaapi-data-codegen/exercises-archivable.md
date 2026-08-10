> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# Exercises.Archivable

> Adds exerciseArchive() to every exercise target. The goal is to correct the problem of having ContractId implement Exercises.makeExerciseCmd(com.daml.ledger.javaapi.data.codegen.Choice<?, ? super A, R>, A) directly. That was a mistake, but one at least obviated by the fact that Exercises.makeExerciseCmd(com.daml.ledger.javaapi.data.codegen.Choice<?, ? super A, R>, A) is clearly part of the internal API, so if you use it directly anyway and you get weird exceptions, you get to keep both pieces of your program. With exerciseArchive() we can correct the problem by having Exercises.Archivable be the real Exercises interface, and the distinction can be flattened when breaking compatibility.

## Exercises.Archivable

Upstream docs: [Open](https://javadoc.io/doc/com.daml/bindings-java/3.5.9/com/daml/ledger/javaapi/data/codegen/Exercises.Archivable.html)

**Signature**

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
public static interface Exercises.Archivable<Cmd> extends Exercises<Cmd>
```

**Members**

| Docs                                                                                                                                             | Member              | Introduced | Deprecated | Removed |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | ---------- | ---------- | ------- |
| [Open](https://javadoc.io/doc/com.daml/bindings-java/3.5.9/com/daml/ledger/javaapi/data/codegen/Exercises.Archivable.html#exerciseArchive%28%29) | `exerciseArchive()` | `3.4.8`    | -          | -       |
