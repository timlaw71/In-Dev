// popup.js
const compoundTlds = [
    'co.jp', 'co.uk', 'co.kr', 'com.au', 'com.br', 'com.cn', 'com.tw', 
    'ne.jp', 'org.uk', 'net.au', 'co.nz', 'com.sg', 'com.hk'
];

function isIpAddress(hostname) {
    // Check for IPv4
    const ipv4Regex = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (ipv4Regex.test(hostname)) {
        const parts = hostname.split('.');
        return parts.every(part => {
            const num = parseInt(part, 10);
            return num >= 0 && num <= 255;
        });
    }
    
    // Check for IPv6
    const ipv6Regex = /^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$/;
    return ipv6Regex.test(hostname);
}

function getTopLevelDomain(hostname) {
    // First check if it's an IP address
    if (isIpAddress(hostname)) {
        return null;
    }

    // Remove www. if present
    let domain = hostname.replace(/^www\./, '');
    
    // Check for compound TLDs first
    for (const tld of compoundTlds) {
        if (domain.endsWith('.' + tld)) {
            const parts = domain.split('.');
            if (parts.length > 2) {
                return parts.slice(-3).join('.');
            }
            return domain;
        }
    }
    
    // Handle regular TLDs
    const parts = domain.split('.');
    if (parts.length > 2) {
        return parts.slice(-2).join('.');
    }
    return domain;
}

function processDomains(urls) {
    const getDomain = (url) => {
        try {
            const urlObj = new URL(url.startsWith('//') ? `https:${url}` : url);
            const hostname = urlObj.hostname.toLowerCase();
            
            // Skip Google domains
            if (hostname.includes('google.com')) {
                return null;
            }
            
            return getTopLevelDomain(hostname);
        } catch (e) {
            console.warn(`Invalid URL: ${url}`);
            return null;
        }
    };

    const uniqueDomains = [...new Set(
        urls
            .map(getDomain)
            .filter(domain => domain !== null)
    )];

    return uniqueDomains.sort();
}

document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "getUrls"}, function(response) {
            if (response && response.urls) {
                const domains = processDomains(response.urls);
                displayDomains(domains);
            }
        });
    });
});

function displayDomains(domains) {
    const domainList = document.getElementById('domainList');
    domainList.innerHTML = '';
    
    domains.forEach(domain => {
        const listItem = document.createElement('div');
        listItem.textContent = domain;
        listItem.className = 'domain-item';
        domainList.appendChild(listItem);
    });
    
    const countElement = document.getElementById('domainCount');
    if (countElement) {
        countElement.textContent = `Found ${domains.length} unique domains`;
    }
}
