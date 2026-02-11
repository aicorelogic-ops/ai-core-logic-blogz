document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-wrapper input');
    const articles = document.querySelectorAll('.article-card');

    if (searchInput) {
        console.log("Search initialized");
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();

            articles.forEach(article => {
                const title = article.querySelector('h2') ? article.querySelector('h2').textContent.toLowerCase() : '';
                const snippet = article.querySelector('.article-snippet') ? article.querySelector('.article-snippet').textContent.toLowerCase() : '';
                const category = article.querySelector('.category-pill') ? article.querySelector('.category-pill').textContent.toLowerCase() : '';

                if (title.includes(searchTerm) || snippet.includes(searchTerm) || category.includes(searchTerm)) {
                    article.style.display = '';
                } else {
                    article.style.display = 'none';
                }
            });
        });
    } else {
        console.warn("Search input not found");
    }
});
