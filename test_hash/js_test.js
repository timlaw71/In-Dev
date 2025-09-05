async function hashFavicon(faviconUrl) {
  try {
    const response = await fetch(faviconUrl, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    // Convert response to Base64
    const arrayBuffer = await response.arrayBuffer();
    const base64 = arrayBufferToBase64(arrayBuffer);

    console.log("JavaScript Base64:", base64); // Compare this output to the Python Base64 string

    let hash = murmurhash3_32_gc(base64, 0); // Seed = 0
    if (hash > 0x7FFFFFFF) {
      hash = hash - 0xFFFFFFFF - 1;
    }

    return hash;
  } catch (error) {
    throw new Error(`Failed to hash favicon: ${error.message}`);
  }
}

