async function analyzeSentiment() {
    const url = document.getElementById('urlInput').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    // Reset UI
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json();

        loadingDiv.classList.add('hidden');

        if (response.ok) {
            document.getElementById('sentimentLabel').innerText = data.sentiment;
            document.getElementById('polarityScore').innerText = data.polarity;
            document.getElementById('subjectivityScore').innerText = data.subjectivity;
            document.getElementById('textExcerpt').innerText = data.excerpt;
            resultDiv.classList.remove('hidden');
        } else {
            errorDiv.innerText = data.error;
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        errorDiv.innerText = "Something went wrong. Ensure the server is running.";
        errorDiv.classList.remove('hidden');
    }
}