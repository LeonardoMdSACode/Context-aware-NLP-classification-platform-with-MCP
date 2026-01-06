async function sendQuery() {
    const queryInput = document.getElementById("query");
    const resultContainer = document.getElementById("result");

    const text = queryInput.value.trim();
    if (!text) {
        resultContainer.innerText = "Please enter some text.";
        return;
    }

    resultContainer.innerText = "Processing...";

    try {
        const response = await fetch(`/predict?query=${encodeURIComponent(text)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        resultContainer.innerText = JSON.stringify(data, null, 2);
    } catch (err) {
        resultContainer.innerText = `Error: ${err.message}`;
    }
}
