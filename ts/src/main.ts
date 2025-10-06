// Application entry point for running the agent
import { logger } from './utils/logger';
import { env } from './utils/env-loader';
import { Blossom } from './spex';
import { SolverProof } from './types';

async function main() {
    logger.info(`Starting SPEX demo application: env=${env.NODE_ENV} log_level=${env.LOG_LEVEL}`);

    // Example usage of the Blossom class
    await demonstrateBlossom();
}

async function demonstrateBlossom() {
    logger.info('=== SPEX Blossom Demo ===');

    // Create a new Blossom instance
    const blossom = new Blossom({
        expectedItems: 100,
        falsePositiveRate: 0.01
    });

    logger.info(`Created Blossom with expected items: ${blossom.getExpectedItems()}`);

    // Add some test data
    const testArrays = [
        [1, 2, 3, 4, 5],
        [10, 20, 30],
        [100, 200, 300, 400],
        [5, 10, 15, 20, 25, 30]
    ];

    logger.info('Adding test arrays to Bloom filter...');
    for (const array of testArrays) {
        blossom.add(array);
        logger.info(`Added array: [${array.join(', ')}]`);
    }

    logger.info(`Total items inserted: ${blossom.getInsertedItems()}`);

    // Test hits
    logger.info('Testing for hits...');
    const testHit = [1, 2, 3, 4, 5];
    const testMiss = [999, 888, 777];

    logger.info(`Array [${testHit.join(', ')}] is hit: ${blossom.isHit(testHit)}`);
    logger.info(`Array [${testMiss.join(', ')}] is hit: ${blossom.isHit(testMiss)}`);

    // Serialize the Bloom filter
    logger.info('Serializing Bloom filter...');
    const serialized = blossom.dump();
    logger.info(`Serialized data length: ${serialized.length} characters`);

    // Create a SolverProof and load it back
    const proof: SolverProof = {
        bloomFilter: Buffer.from(serialized, 'base64'),
        countItems: blossom.getInsertedItems()
    };

    logger.info('Loading Bloom filter from proof...');
    const loadedBlossom = Blossom.load(proof);
    logger.info(`Loaded Blossom with ${loadedBlossom.getInsertedItems()} items`);

    // Verify the loaded filter works the same
    logger.info(`Loaded filter - Array [${testHit.join(', ')}] is hit: ${loadedBlossom.isHit(testHit)}`);
    logger.info(`Loaded filter - Array [${testMiss.join(', ')}] is hit: ${loadedBlossom.isHit(testMiss)}`);

    // Estimate false positive rate
    logger.info('Estimating false positive rate...');
    const falsePositiveRate = blossom.estimateFalsePositiveRate();
    logger.info(`Estimated false positive rate: ${falsePositiveRate.toFixed(6)}`);

    // Verify false positive rate
    const isVerified = blossom.verifyFalsePositiveRate(0.01, 0.01);
    logger.info(`False positive rate verification: ${isVerified ? 'PASSED' : 'FAILED'}`);

    logger.info('=== SPEX Blossom Demo Complete ===');

}
/////////////////////////////////////////////////////

// Handle errors
process.on('unhandledRejection', (error) => {
    logger.error('Unhandled rejection:', error);
    process.exit(1);
});

process.on('uncaughtException', (error) => {
    logger.error('Uncaught exception:', error);
    process.exit(1);
});

// Run main function if this is the entry point
if (require.main === module) {
    main().catch((error) => {
        logger.error('Fatal error:', error);
        process.exit(1);
    });
}