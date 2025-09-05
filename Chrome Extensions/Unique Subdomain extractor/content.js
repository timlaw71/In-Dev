// content.js
function getAllUrls() {
    // Get all search result links from Google
    const searchResults = document.querySelectorAll('a');
    const urls = Array.from(searchResults)
        .map(a => a.href)
        .filter(url => url && !url.startsWith('javascript:') && !url.startsWith('chrome-extension://'));
    
    // Send URLs to popup when requested
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "getUrls") {
            sendResponse({ urls: urls });
        }
    });
}

// Run when page loads
getAllUrls();
