export async function fetchCheckInformation(checkInformation, information) {
    const apiURL = `/authors/api/check-${checkInformation}/`;

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            [checkInformation]: information
        }),
    };

    try {
        const response = await fetch(apiURL, options);

        if (!response.ok) {
            console.error(`Error in API: ${response.status} ${response.statusText}`);
            return null;
        }

        const data = await response.json();

        return data;

    } catch(error) {
        console.error('Request Error', error);
    }
};
