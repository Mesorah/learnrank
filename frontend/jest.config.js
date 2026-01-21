export default {
    testEnvironment: 'jsdom',
    setupFiles: ['<rootDir>/jest.setup.js'],

    collectCoverage: true,
    collectCoverageFrom: [
        '<rootDir>/../authors/static/authors/js/**/*.js',
        '<rootDir>/../courses/static/courses/js/**/*.js',
        '!<rootDir>/__tests__/**',
    ],

    moduleNameMapper: {
        '^@jsAuthors/(.*)$': '<rootDir>/../authors/static/authors/js/$1',
        '^@jsCourses/(.*)$': '<rootDir>/../courses/static/courses/js/$1',
    },

    coverageReporters: ['text', 'html'],
};
