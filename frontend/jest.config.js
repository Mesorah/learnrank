export default {
    testEnvironment: 'jsdom',
    setupFiles: ['<rootDir>/jest.setup.js'],

    collectCoverage: true,
    collectCoverageFrom: [
        '<rootDir>/../authors/static/authors/js/**/*.js',
        '!<rootDir>/__tests__/**',
    ],

    moduleNameMapper: {
        '^@jsAuthors/(.*)$': '<rootDir>/../authors/static/authors/js/$1',
    },

    coverageReporters: ['text', 'html'],
};
