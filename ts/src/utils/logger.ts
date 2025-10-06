import { env } from './env-loader';
import * as fs from 'fs';
import * as path from 'path';

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

const logLevels: Record<LogLevel, number> = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
};

class Logger {
    private level: number;
    private logFilePath: string;

    constructor() {
        this.level = logLevels[env.LOG_LEVEL] || logLevels.INFO;
        this.logFilePath = path.join(process.cwd(), 'spex.log');

        // Ensure log directory exists
        const logDir = path.dirname(this.logFilePath);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
    }

    private shouldLog(level: LogLevel): boolean {
        return logLevels[level] >= this.level;
    }

    private formatMessage(level: LogLevel, message: string, data?: any): string {
        const timestamp = new Date().toISOString();
        const prefix = `[${timestamp}] [${level.toUpperCase()}]`;

        if (data) {
            return `${prefix} ${message} ${JSON.stringify(data, null, 2)}`;
        }

        return `${prefix} ${message}`;
    }

    private writeToFile(message: string): void {
        try {
            fs.appendFileSync(this.logFilePath, message + '\n');
        } catch (error) {
            // Fallback to console if file writing fails
            console.error('Failed to write to log file:', error);
        }
        // Always output to console as well
        console.log(message);
    }

    debug(message: string, data?: any): void {
        if (this.shouldLog('DEBUG')) {
            const formattedMessage = this.formatMessage('DEBUG', message, data);
            this.writeToFile(formattedMessage);
        }
    }

    info(message: string, data?: any): void {
        if (this.shouldLog('INFO')) {
            const formattedMessage = this.formatMessage('INFO', message, data);
            this.writeToFile(formattedMessage);
        }
    }

    warn(message: string, data?: any): void {
        if (this.shouldLog('WARN')) {
            const formattedMessage = this.formatMessage('WARN', message, data);
            this.writeToFile(formattedMessage);
        }
    }

    error(message: string, error?: any): void {
        if (this.shouldLog('ERROR')) {
            const errorData = error instanceof Error
                ? { message: error.message, stack: error.stack }
                : error;
            const formattedMessage = this.formatMessage('ERROR', message, errorData);
            this.writeToFile(formattedMessage);
        }
    }
}

export const logger = new Logger();
