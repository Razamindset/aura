document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const searchButton = document.getElementById("search-button");
  const resultsDiv = document.getElementById("results");
  const themeSwitch = document.getElementById("checkbox");
  const body = document.body;

  // Theme switcher logic
  const currentTheme = localStorage.getItem("theme");
  if (currentTheme) {
    body.classList.add("dark-mode");
    themeSwitch.checked = true;
  }

  themeSwitch.addEventListener("change", () => {
    if (body.classList.contains("dark-mode")) {
      body.classList.remove("dark-mode");
      localStorage.removeItem("theme");
    } else {
      body.classList.add("dark-mode");
      localStorage.setItem("theme", "dark-mode");
    }
  });

  // Search logic
  searchButton.addEventListener("click", performSearch);
  searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      performSearch();
    }
  });

  async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) {
      resultsDiv.innerHTML = '<p class="error">Please enter a search query.</p>';
      body.classList.remove("results-shown");
      return;
    }

    showLoader();

    try {
      const response = await fetch(
        `/search?query=${encodeURIComponent(query)}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error("Error during search:", error);
      resultsDiv.innerHTML =
        '<p class="error">Error performing search. Please try again later.</p>';
      body.classList.remove("results-shown");
    }
  }

  function showLoader() {
    resultsDiv.innerHTML = `
      <div class="loader">
        <p>Searching...</p>
      </div>
    `;
  }

  function displayResults(results) {
    resultsDiv.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
      resultsDiv.innerHTML = "<p>No results found.</p>";
      body.classList.remove("results-shown");
      return;
    }

    body.classList.add("results-shown");

    results.forEach((result) => {
      const resultItem = document.createElement("div");
      resultItem.classList.add("result-item");

      const title = document.createElement("h3");
      const link = document.createElement("a");
      link.href = result.url;
      link.textContent = result.title;
      link.target = "_blank";

      const icon = document.createElement("img");
      icon.src = result.icon_url || 'placeholder.svg'; // Add a placeholder
      icon.alt = "";

      title.appendChild(icon);
      title.appendChild(link);

      const url = document.createElement("p");
      url.classList.add("url");
      url.textContent = result.url;

      const description = document.createElement("p");
      description.textContent = result.description || "No description available.";

      resultItem.appendChild(title);
      resultItem.appendChild(url);
      resultItem.appendChild(description);

      resultsDiv.appendChild(resultItem);
    });
  }
});