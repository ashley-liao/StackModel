chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "dataReceived"){
        chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icon.png', 
                title: 'Data Received',
                message: 'Successfully fetched data.', // Customize this message if needed
                contextMessage: JSON.stringify(message.data).substring(0, 100) + '...' // Show a preview of the data; adjust length as needed
            });
    }
});