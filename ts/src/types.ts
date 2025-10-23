/**
 * TypeScript types and interfaces for SPEX (Statistical Proof of Execution)
 * Based on the Python implementation in warden_spex.models
 */

// Generic types for solver input/output
export type TypeSolverInput = any;
export type TypeSolverOutput = any;

/**
 * Base interface for all SPEX models
 */
export interface BaseModel {
    // Common properties can be added here
}

/**
 * Solver request with inputs and quality guarantees
 */
export interface SolverRequest<T extends TypeSolverInput = TypeSolverInput> extends BaseModel {
    solverInput?: T;
    falsePositiveRate: number; // 0-1 range, default 0.01
}

/**
 * Solver proof containing bloom filter and item count
 */
export interface SolverProof extends BaseModel {
    bloomFilter: Uint8Array; // Base64 encoded bytes
    countItems: number; // >= 0, default 1
}

/**
 * Solver response with output and proof
 */
export interface SolverResponse<T extends TypeSolverOutput = TypeSolverOutput> extends BaseModel {
    solverOutput?: T;
    solverProof: SolverProof;
}

/**
 * Verifier request with solver request, output, proof and verification ratio
 */
export interface VerifierRequest<T extends TypeSolverOutput = TypeSolverOutput> extends BaseModel {
    solverRequest: SolverRequest;
    solverOutput?: T;
    solverProof: SolverProof;
    verificationRatio: number; // 0-1 range, default 0.1
}

/**
 * Verifier response with verification results
 */
export interface VerifierResponse extends BaseModel {
    countItems: number; // >= 0, default 1
    isVerified: boolean; // default false
    evidence?: string;
}

/**
 * Abstract task interface for solver and verifier implementations
 */
export interface Task<TInput extends TypeSolverInput = TypeSolverInput, TOutput extends TypeSolverOutput = TypeSolverOutput> {
    solve(request: SolverRequest<TInput>): SolverResponse<TOutput>;
    verify(request: VerifierRequest<TOutput>): VerifierResponse;
}

/**
 * Custom exception for invalid values
 */
export class InvalidValueException extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'InvalidValueException';
    }
}

/**
 * Configuration options for Blossom (Bloom filter)
 */
export interface BlossomConfig {
    expectedItems?: number; // default 1000
    falsePositiveRate?: number; // default 0.01
}

/**
 * Array type for numeric arrays (equivalent to numpy arrays)
 */
export type NumericArray = number[] | Int32Array | Float64Array | Uint8Array;
