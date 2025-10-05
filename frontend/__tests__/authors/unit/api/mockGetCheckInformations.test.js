import fetchMock from 'jest-fetch-mock';
fetchMock.enableMocks();

import { fetchCheckEmail } from "@js/getCheckEmailAPI";
import { fetchCheckUsername } from "@js/getCheckUsernameAPI";

beforeEach(() => {
    fetch.resetMocks();
});

describe('Check username API using mock', () => {
    test('should success is true if username do not exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({
            username_already_registred: false
        }))
        const result = await fetchCheckUsername('usernameDoNotExists');

        expect(result.username_already_registred).toBe(false);
    });

    test('should success is false if username exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({
            username_already_registred: true
        }))
        const result = await fetchCheckUsername('usernameExists');

        expect(result.username_already_registred).toBe(true);
    });
});

describe('Check email API using mock', () => {
    test('should success is true if email do not exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({
            email_already_registred: false
        }))
        const result = await fetchCheckEmail('emailDoNotExists');

        expect(result.email_already_registred).toBe(false);
    });

    test('should success is false if email exists', async() => {
        fetch.mockResponseOnce(JSON.stringify({
            email_already_registred: true
        }))
        const result = await fetchCheckEmail('emailExists');

        expect(result.email_already_registred).toBe(true);
    });
});