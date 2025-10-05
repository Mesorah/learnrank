const apiURL = 'http://127.0.0.1:8000/authors/api/check-email/';

export async function fetchCheckEmail(email) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            email: email
        }),
    };

    try {
        const response = await fetch(apiURL, options);

        if (!response.ok) {
            console.error(`Error in API: ${response.status} ${response.statusText}`);
            return null;
        }

        const data = await response.json();
        console.log('Return API:', data);

        return data;

    } catch(error) {
        console.error('Request Error', error);
    }
};
