# Statistical Proof of Execution (SPEX)

The protocol is formally described in the whitepaper "Statistical Proof of Execution (SPEX)" by Michele Dallachiesa, Antonio Pitasi, David Pinger, Josh Goodbody, and Luis Vaello: [http://arxiv.org/abs/2503.18899](http://arxiv.org/abs/2503.18899).

**SPEX** (Statistical Proof of Execution) is a novel protocol for verifiable computing that provides correctness guarantees through probabilistic sampling. Designed for workloads that include non-deterministic outputs—such as AI inference, LLMs, or floating-point computations—SPEX introduces a lightweight, cost-effective alternative to traditional methods like ZKPs or TEEs.

As AI/ML becomes embedded in critical infrastructure, the need for transparent and auditable computation has never been more urgent. SPEX addresses this by enabling solvers to generate compact cryptographic proofs (via Bloom filters) of their computations. Verifiers can then validate correctness with statistical confidence, without having to re-execute entire workloads.

Key features include:
- **Sampling-based verification** with tunable confidence levels
- **Support for non-determinism**, including semantically similar embeddings and agentic plans
- **Low overhead** and **full parallelizability** of solvers and verifiers
- **Open-source** reference implementation in [`warden-spex`](https://github.com/warden-protocol/warden-spex)

SPEX is particularly suited for cloud, edge, and blockchain environments where computation outsourcing and trust minimization are crucial.

## Problem definition

SPEX addresses the problem of **verifiable computing**: how can a verifier efficiently and probabilistically ensure that a computation performed by an untrusted solver was executed correctly?

Formally, given a task *t* (for example, model inference, data processing pipeline), we aim to guarantee that its output *r* is correct with high confidence, without requiring full re-execution by the verifier. This is especially challenging in cases where:
- The solver may act **lazily** (skipping computation)
- Or **adversarially** (producing plausible but incorrect outputs)
- The task may be **non-deterministic** (for example, due to floating point instability, randomness, or LLM behavior)

The goal is to design a protocol in which:
- A **solver** executes task *t* and emits both the result and a **cryptographic proof** (for example, via a Bloom filter)
- A **verifier** uses sampling and statistics to check that the result is correct, with confidence level

SPEX minimizes memory and compute overhead for both parties, making it suitable for scalable, parallelizable, and real-world AI workloads where full re-execution is impractical.

## Install SPEX

To install SPEX, run the following:

```
pip install warden_spex --upgrade
```

**Important**: SPEX is progressing rapidly and interfaces might change at any time. To make sure your project remains functional, pin a specific SPEX version. Before updating the project, test it and verify that everything works correctly.

## Define a new task in SPEX

To integrate a new task into the SPEX protocol, you need to implement two core components: the **solver** and the **verifier**. They operate on the SPEX request/response interfaces and must be tailored to your specific computational workload.

### 1. Define the task logic

A *task* is any function or pipeline you want to verify—for example, model inference or data transformation. The core logic must be wrapped in a **solver function** that does the following:
- Accepts a `SolverRequest` (input data and false positive rate)
- Computes the task output
- Inserts computational states into a Bloom filter as cryptographic proof
- Returns a `SolverResponse` with both result and proof

### 2. Implement the verifier

The **verifier function** should solve these tasks:
- Take a `VerifierRequest` with the original inputs, solver outputs, and proof
- Sample computational states based on a configurable confidence level
- Check sampled states against the Bloom filter
- Return a `VerifierResponse` indicating verification status and evidence if needed

### 3. Define the sampling strategy

Choose appropriate computational states to insert into the Bloom filter:
- For deterministic tasks: hash discrete values or intermediate outputs
- For floating-point or embedding-based tasks: apply robust or semantic hashing
- For agentic or procedural outputs: hash structured execution plans

Refer to the `PrimeSum` example in the repository ([test_spex.py](https://github.com/warden-protocol/warden-spex/blob/main/tests/test_spex.py)) for a fully working task definition. For advanced workloads, SPEX also supports flexible handling of non-determinism through fuzzy or semantic state matching.

## LICENSE

```
Copyright 2024,2025 Warden Protocol <https://wardenprotocol.org/>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

