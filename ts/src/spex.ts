/**
 * TypeScript implementation of SPEX (Statistical Proof of Execution)
 * Inspired by the Python implementation in warden_spex.spex
 */

import { BloomFilter } from 'bloom-filters';
import {
    BlossomConfig,
    InvalidValueException,
    NumericArray,
    SolverProof,
} from './types';

/**
 * Maximum number of hash functions allowed in Bloom filter configuration
 */
const MAX_HASH_FUNCTIONS = 10;

/**
 * Convert a numeric array or typed array into a string for hashing consistency
 */
function arrayToString(array: NumericArray): string {
    return Array.isArray(array)
        ? array.join(',')
        : Array.from(array).join(',');
}

/**
 * Compute optimal Bloom filter parameters based on expected item count and desired false positive rate.
 * Reference: https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions
 */
function computeBloomParams(expectedItems: number, falsePositiveRate: number) {
    const m = Math.ceil(
        -(expectedItems * Math.log(falsePositiveRate)) / Math.log(2) ** 2,
    );
    const k = Math.ceil((m / expectedItems) * Math.log(2));

    if (k > MAX_HASH_FUNCTIONS) {
        throw new Error(
            `Invalid configuration: computed ${k} hash functions (max ${MAX_HASH_FUNCTIONS}). 
       Try increasing 'falsePositiveRate' or reducing 'expectedItems'.`,
        );
    }

    return { m, k };
}

/**
 * Extended Bloom filter implementation with SPEX-related utilities.
 */
export class Blossom {
    private insertedItems = 0;
    private expectedItems: number;
    private bloom: BloomFilter;

    constructor(config: BlossomConfig = {}) {
        const { expectedItems = 1000, falsePositiveRate = 0.01 } = config;

        this.expectedItems = expectedItems;
        const { m, k } = computeBloomParams(expectedItems, falsePositiveRate);
        this.bloom = new BloomFilter(m, k);
    }

    /**
     * Serialize Bloom filter to Base64-encoded JSON
     */
    dump(): string {
        const serialized = this.bloom.saveAsJSON();
        return Buffer.from(JSON.stringify(serialized), 'utf-8').toString('base64');
    }

    /**
     * Test whether a given array is present in the Bloom filter
     */
    isHit(array: NumericArray): boolean {
        return this.bloom.has(arrayToString(array));
    }

    /**
     * Insert an array into the Bloom filter
     */
    add(array: NumericArray): void {
        if (this.insertedItems >= this.expectedItems) {
            throw new InvalidValueException(
                `Bloom filter capacity exceeded (expectedItems=${this.expectedItems}). 
         Consider increasing 'expectedItems' in the configuration.`,
            );
        }

        this.insertedItems++;
        this.bloom.add(arrayToString(array));
    }

    /**
     * Insert multiple arrays into the Bloom filter
     */
    addItems(items: Iterable<NumericArray>): void {
        for (const item of items) this.add(item);
    }

    /**
     * Deserialize a Bloom filter from a proof object
     */
    static load(proof: SolverProof): Blossom {
        if (!proof?.bloomFilter || typeof proof.countItems !== 'number') {
            throw new InvalidValueException('Invalid SolverProof structure.');
        }

        const decoded = Buffer.from(proof.bloomFilter).toString('utf-8');
        const bloomData = JSON.parse(decoded);

        const blossom = new Blossom();
        blossom.bloom = BloomFilter.fromJSON(bloomData);
        blossom.insertedItems = proof.countItems;

        return blossom;
    }

    /**
     * Estimate the empirical false positive rate through sampling
     * @param sampleSize Number of random trials to perform (default: 10,000)
     */
    estimateFalsePositiveRate(sampleSize = 10_000): number {
        let hits = 0;

        const rand = ((): number => {
            if (typeof crypto !== 'undefined' && 'getRandomValues' in crypto) {
                const buf = new Uint32Array(1);
                crypto.getRandomValues(buf);
                return buf[0]!;
            }
            return Math.floor(Math.random() * 2 ** 32);
        });

        for (let i = 0; i < sampleSize; i++) {
            const key = rand().toString();
            if (this.bloom.has(key)) hits++;
        }

        return hits / sampleSize;
    }

    /**
     * Verify that the observed false positive rate is within an acceptable range
     */
    verifyFalsePositiveRate(
        expectedRate = 0.01,
        tolerance = 0.01,
    ): boolean {
        const estimated = this.estimateFalsePositiveRate();
        console.debug(`Bloom FPR check: estimated=${estimated}, expected=${expectedRate}, tolerance=${tolerance}`);
        return estimated <= expectedRate + tolerance;
    }

    /**
     * Return the number of inserted items
     */
    getInsertedItems(): number {
        return this.insertedItems;
    }

    /**
     * Return the configured expected number of items
     */
    getExpectedItems(): number {
        return this.expectedItems;
    }
}