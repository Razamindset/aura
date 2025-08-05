document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsDiv = document.getElementById('results');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    async function performSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            resultsDiv.innerHTML = '<p>Please enter a search query.</p>';
            return;
        }

        resultsDiv.innerHTML = '<p>Searching...</p>';

        try {
            // Assuming your backend will expose a /search endpoint
            const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            displayResults(data);
        } catch (error) {
            console.error('Error during search:', error);
            resultsDiv.innerHTML = '<p>Error performing search. Please try again later.</p>';
        }
    }

    function displayResults(results) {
        resultsDiv.innerHTML = ''; // Clear previous results

        if (results.length === 0) {
            resultsDiv.innerHTML = '<p>No results found.</p>';
            return;
        }

        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');

            const title = document.createElement('h3');
            const link = document.createElement('a');
            link.href = result.url; // Assuming 'url' field in your search result object
            link.textContent = result.title; // Assuming 'title' field
            link.target = '_blank'; // Open in new tab
            title.appendChild(link);

            const url = document.createElement('p');
            url.classList.add('url');
            url.textContent = result.url;

            const description = document.createElement('p');
            description.textContent = result.description; // Assuming 'description' field

            resultItem.appendChild(title);
            resultItem.appendChild(url);
            resultItem.appendChild(description);

            resultsDiv.appendChild(resultItem);
        });
    }
});