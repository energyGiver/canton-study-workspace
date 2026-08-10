> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying a Private Synchronizer

> Step-by-step guide for deploying sequencer and mediator nodes for a private Canton synchronizer

A private synchronizer requires deploying sequencer and mediator nodes, configuring their database backends, and connecting validators. This guide covers the infrastructure setup for both standalone and hybrid deployments.

## Prerequisites

Before you begin:

* A Kubernetes cluster (1.27+) with Helm 3 installed
* PostgreSQL 14+ (managed service recommended for production)
* TLS certificates for the sequencer endpoint
* Canton release artifacts (Docker images or JARs)
* Familiarity with [Canton's synchronizer architecture](/overview/reference/synchronizer-overview)

## Ordering backends

The sequencer requires a backend to store and order messages. Canton supports two options:

* **Centralized ordering** — A single ordering node acts as the ordering backend. Simpler to operate, suitable for private synchronizers where a single operator manages the infrastructure. Currently in **Alpha**.
* **Decentralized ordering (BFT with CometBFT)** — Multiple sequencer nodes run BFT consensus. Required when multiple independent parties operate the synchronizer and no single party should control ordering. This is how the Global Synchronizer operates.

For most private synchronizer deployments where a single organization controls the infrastructure, the centralized ordering backend is the simpler choice.

## Database setup

You need separate PostgreSQL databases for the sequencer and mediator. Each node stores its own state independently.

Create separate databases (`sequencer_db`, `mediator_db`) with dedicated users. For production, use a managed PostgreSQL service (Cloud SQL, RDS, Azure Database for PostgreSQL) with automated backups, high availability, at least 4 vCPUs / 16 GB memory, and SSD-backed storage.

## Deploying the sequencer

### Helm chart configuration

Create a values file for the sequencer:

```yaml theme={"theme":{"light":"github-light","dark":"github-dark"}}
# sequencer-values.yaml
sequencer:
  storage:
    type: postgres
    config:
      dataSourceClass: "org.postgresql.ds.PGSimpleDataSource"
      properties:
        serverName: "<postgres-host>"
        portNumber: 5432
        databaseName: "sequencer_db"
        user: "sequencer_user"
        password: "<password>"
  publicApi:
    tls:
      certChainFile: "/certs/tls.crt"
      privateKeyFile: "/certs/tls.key"
  parameters:
    synchronizerName: "my-private-sync"
```

Deploy with Helm:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
helm install sequencer canton/canton-sequencer \
  -f sequencer-values.yaml \
  --namespace canton-sync
```

## Deploying the mediator

Create a values file for the mediator:

```yaml theme={"theme":{"light":"github-light","dark":"github-dark"}}
# mediator-values.yaml
mediator:
  storage:
    type: postgres
    config:
      dataSourceClass: "org.postgresql.ds.PGSimpleDataSource"
      properties:
        serverName: "<postgres-host>"
        portNumber: 5432
        databaseName: "mediator_db"
        user: "mediator_user"
        password: "<password>"
  sequencerConnection:
    address: "https://sequencer.canton-sync.svc.cluster.local"
```

Deploy with Helm:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
helm install mediator canton/canton-mediator \
  -f mediator-values.yaml \
  --namespace canton-sync
```

## Initializing the synchronizer

After both nodes are running, initialize the synchronizer topology. Using the Canton Console connected to the sequencer:

```scala theme={"theme":{"light":"github-light","dark":"github-dark"}}
@ bootstrap.synchronizer(synchronizerName = "my-private-sync", sequencers = Seq(sequencer1), mediators = Seq(mediator1), synchronizerOwners = Seq(sequencer1), synchronizerThreshold = PositiveInt.one, staticSynchronizerParameters = StaticSynchronizerParameters.defaultsWithoutKMS(ProtocolVersion.forSynchronizer))
    res1: PhysicalSynchronizerId = my-private-sync::122032922613...::35-0
```

This creates the synchronizer identity and registers the sequencer and mediator in the synchronizer topology.

## Connecting validators

Once the synchronizer is initialized, validators can connect to it. On each validator's Canton Console:

```scala theme={"theme":{"light":"github-light","dark":"github-dark"}}
@ participant1.synchronizers.connect_local(sequencer1, "my-private-sync")
```

Or configure the connection in the validator's Helm values:

```yaml theme={"theme":{"light":"github-light","dark":"github-dark"}}
participant:
  additionalSynchronizerConnections:
    - alias: "my-private-sync"
      sequencerConnection: "https://sequencer.private-sync.example.com"
```

After connecting, verify the connection with `participant.synchronizers.list_connected()`.

## Verification

Confirm end-to-end functionality by allocating a test party and creating a contract on the private synchronizer. Check the sequencer health endpoint (HTTP 200 means ready) and verify the mediator is registered in the synchronizer topology.

## Production considerations

* **TLS everywhere** — Use TLS for all connections between validators and the synchronizer
* **Network policies** — Restrict sequencer endpoint access to known validator IPs
* **Monitoring** — Sequencer and mediator nodes expose Prometheus metrics; use the same monitoring stack as your validators
* **Backups** — Back up sequencer and mediator databases regularly

<Warning>
  The centralized ordering backend (PostgreSQL) is in Alpha. For production workloads, test thoroughly with your expected transaction volume and plan for the possibility of breaking changes in future Canton releases.
</Warning>
