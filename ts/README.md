# SPEX TypeScript Implementation

A TypeScript implementation of **SPEX** (Statistical Proof of Execution). This implementation is based on the Python reference implementation in [`warden-spex`](https://github.com/warden-protocol/warden-spex).

For the complete protocol description, see the main [README.md](../README.md).

## Key Features

- **Type-safe interfaces** with full TypeScript support
- **Runtime type validation** with Zod for environment and input validation
- **Bloom filter implementation** (`Blossom` class) with optimal parameter computation
- **Cross-platform compatibility** (Node.js, browsers with crypto support)

## Installation

```bash
cp .env.template .env
make install
```

## Quick Start

### Running the Demo

```bash
make demo
```

This demonstrates the SPEX TypeScript implementation including Bloom filter operations, serialization, and verification.

### Environment Configuration

The implementation includes environment management with validation. Create a `.env` file:

```
LOG_LEVEL=INFO
```

## API Reference

### Blossom Class

The core Bloom filter implementation with SPEX-specific utilities.

#### Constructor
`new Blossom(config?: BlossomConfig)`

**Configuration Options:**
- `expectedItems` (default: 1000): Expected number of items to be inserted
- `falsePositiveRate` (default: 0.01): Desired false positive rate (0-1)

#### Methods
- `add(array: NumericArray): void` - Insert an array into the Bloom filter
- `addItems(items: Iterable<NumericArray>): void` - Insert multiple arrays
- `isHit(array: NumericArray): boolean` - Test if an array is present
- `dump(): string` - Serialize to Base64-encoded JSON
- `estimateFalsePositiveRate(sampleSize?: number): number` - Estimate empirical FPR
- `verifyFalsePositiveRate(expectedRate?: number, tolerance?: number): boolean` - Verify FPR
- `getInsertedItems(): number` - Get count of inserted items
- `getExpectedItems(): number` - Get configured expected items

#### Static Methods
- `Blossom.load(proof: SolverProof): Blossom` - Deserialize from proof object

### Type Definitions

#### Core Interfaces
- `SolverRequest<T>` - Solver request with inputs and quality guarantees
- `SolverProof` - Solver proof containing bloom filter and item count
- `SolverResponse<T>` - Solver response with output and proof
- `VerifierRequest<T>` - Verifier request with solver data and verification ratio
- `VerifierResponse` - Verifier response with verification results

#### Utility Types
- `NumericArray` - Array type for numeric arrays (number[], Int32Array, Float64Array, Uint8Array)
- `TypeSolverInput` - Generic solver input type
- `TypeSolverOutput` - Generic solver output type

## Implementation Details

### Bloom Filter Optimization
Automatically computes optimal Bloom filter parameters based on expected items and desired false positive rate using standard Bloom filter theory.

### Cross-Platform Random Number Generation
Uses Web Crypto API when available (browsers) and falls back to `Math.random()` for Node.js environments.

### Error Handling
Custom `InvalidValueException` class for better error handling.

## Dependencies

- `bloom-filters`: Bloom filter implementation
- `dotenv`: Environment variable management
- `zod`: Runtime type validation

## License

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