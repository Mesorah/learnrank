import fetchMock from 'jest-fetch-mock';
fetchMock.enableMocks();

import { fetchCheckUsername } from '@js/getCheckUsernameAPI';

beforeEach(() => {
    fetch.resetMocks();
});

describe('Check username API using mock', () => {
    test('should success is true if username do not exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({result: true}))
        const result = await fetchCheckUsername('usernameDoNotExists');

        expect(result.result).toBe(true);
    });

    test('should success is false if username exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({result: false}))
        const result = await fetchCheckUsername('usernameExists');

        expect(result.result).toBe(false);
    })
});
