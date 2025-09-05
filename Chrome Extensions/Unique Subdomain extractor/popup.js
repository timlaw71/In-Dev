// popup.js
function getFullDomain(hostname) {
    // Remove www. prefix if present, keep everything else including IPs
    return hostname.replace(/^www\./, '');
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
            
            return getFullDomain(hostname);
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

    // Sort domains with IPs and subdomains
    return uniqueDomains.sort((a, b) => {
        // Check if either is an IP address
        const isIpA = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(a);
        const isIpB = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(b);
        
        // If both are IPs, sort numerically by octets
        if (isIpA && isIpB) {
            const aOctets = a.split('.').map(Number);
            const bOctets = b.split('.').map(Number);
            for (let i = 0; i < 4; i++) {
                if (aOctets[i] !== bOctets[i]) {
                    return aOctets[i] - bOctets[i];
                }
            }
            return 0;
        }
        
        // If only one is an IP, sort IPs first
        if (isIpA) return -1;
        if (isIpB) return 1;
        
        // For domains, sort by reversed parts
        const aParts = a.split('.').reverse();
        const bParts = b.split('.').reverse();
        
        for (let i = 0; i < Math.min(aParts.length, bParts.length); i++) {
            if (aParts[i] !== bParts[i]) {
                return aParts[i].localeCompare(bParts[i]);
            }
        }
        
        return aParts.length - bParts.length;
    });
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
        
        // Add special styling for IPs and subdomains
        if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(domain)) {
            listItem.classList.add('is-ip');
        } else if (domain.split('.').length > 2) {
            listItem.classList.add('has-subdomain');
        }
        
        domainList.appendChild(listItem);
    });
    
    const countElement = document.getElementById('domainCount');
    if (countElement) {
        countElement.textContent = `Found ${domains.length} unique domains/IPs`;
    }
}