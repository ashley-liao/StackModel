const url = window.location.href;
const htmlContent = document.documentElement.outerHTML;
fetch('http://localhost:4765/receive_data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url: url, html: htmlContent }),
})
.then(response => response.json())
.then(data => chrome.runtime.sendMessage({type: "dataReceived", data: data}))

