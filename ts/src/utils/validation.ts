// src/utils/validation.ts
import { z } from 'zod';

// Validate input against a schema
export function validateInput<T>(
    input: unknown,
    schema: z.ZodSchema<T>
): { success: true; data: T } | { success: false; errors: string[] } {
    try {
        const data = schema.parse(input);
        return { success: true, data };
    } catch (error) {
        if (error instanceof z.ZodError) {
            const errors = error.errors.map(e => `${e.path.join('.')}: ${e.message}`);
            return { success: false, errors };
        }
        return { success: false, errors: ['Unknown validation error'] };
    }
}

// Sanitize string input
export function sanitizeString(input: string, maxLength: number = 1000): string {
    // Remove control characters
    let sanitized = input.replace(/[\x00-\x1F\x7F]/g, '');

    // Trim whitespace
    sanitized = sanitized.trim();

    // Limit length
    if (sanitized.length > maxLength) {
        sanitized = sanitized.substring(0, maxLength);
    }

    return sanitized;
}
