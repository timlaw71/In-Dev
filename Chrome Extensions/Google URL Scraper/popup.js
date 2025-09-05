function extractURLs() {
  // Extract all links, then filter out any URLs that contain "google.com"
  return Array.from(document.querySelectorAll('a'))
    .map(link => link.href)
    .filter(url => !url.includes('google.com'));
}

// Run the URL extraction when the popup is opened
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  chrome.scripting.executeScript({
    target: { tabId: tabs[0].id },
    func: extractURLs,
  }, (results) => {
    if (results && results[0]) {
      const urls = results[0].result;
      displayURLs(urls);
      saveURLs(urls);
    }
  });
});

// Display URLs as before
function displayURLs(urls) {
  const urlList = document.getElementById('urlList');
  urlList.innerHTML = ''; // Clear existing list
  urls.forEach(url => {
    const listItem = document.createElement('li');
    const link = document.createElement('a');
    link.href = url;
    link.textContent = url;
    link.target = '_blank';
    listItem.appendChild(link);
    urlList.appendChild(listItem);
  });
}

// Save URLs to local storage
function saveURLs(urls) {
  chrome.storage.local.set({ extractedURLs: urls }, () => {
    console.log('URLs saved to local storage.');
  });
}

// Load and display saved URLs if available
chrome.storage.local.get(['extractedURLs'], (data) => {
  if (data.extractedURLs) {
    displayURLs(data.extractedURLs);
  }
});

// Optional: Button to export URLs to a text file
document.getElementById('exportBtn').addEventListener('click', () => {
  chrome.storage.local.get(['extractedURLs'], (data) => {
    if (data.extractedURLs) {
      downloadURLs(data.extractedURLs);
    }
  });
});

// Function to download URLs as a text file
function downloadURLs(urls) {
  const blob = new Blob([urls.join('\n')], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'extracted_urls.txt';
  link.click();
  URL.revokeObjectURL(url);
}
