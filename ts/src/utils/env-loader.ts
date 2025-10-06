// src/config/index.ts
import dotenv from 'dotenv';
import { z } from 'zod';

// Load environment variables
dotenv.config({ quiet: true });

// Define environment schema for validation
const envSchema = z.object({
    LOG_LEVEL: z.enum(['DEBUG', 'INFO', 'WARN', 'ERROR']).default('INFO'),
});


// Parse and validate environment variables
const parseEnv = () => {
    try {
        return envSchema.parse(process.env);
    } catch (error) {
        console.error('Invalid environment variables:', error);
        process.exit(1);
    }
};

export const env = parseEnv();

export type EnvironmentType = z.infer<typeof envSchema>;
