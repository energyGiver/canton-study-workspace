> ## Documentation Index
> Fetch the complete documentation index at: https://docs.canton.network/llms.txt
> Use this file to discover all available pages before exploring further.

# Validator Ingress and Egress Requirements

> Network ingress and egress requirements for validator nodes

## Ingress

The validators have no external ingress requirements and don't need to whitelist any other SVs or validators.

## Egress

The validators must be able to connect to all the SVs, thus whitelisting of egress on port 443 for the IPs of all the SVs is required (refer to [the network diagram](/global-synchronizer/deployment/validator-kubernetes) for a networking overview). Note that egress is often allowed by default, so in many cases this requires no action.
