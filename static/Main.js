// Function to handle scraping data
function scrapeData() {
    const cityInput = document.getElementById('cityInput').value;
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `city=${cityInput}`,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok (${response.status})`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Data received:", data);
        updateScrapedData(data);
    })
    .catch(error => {
        console.error('Error scraping data:', error);
        // Display an error message in the container
        const scrapedDataContainer = document.getElementById('scrapedDataContainer');
        scrapedDataContainer.innerHTML = `<p>Error scraping data: ${error.message || 'Unknown error'}</p>`;
    });
}

// Function to update the DOM with scraped data
function updateScrapedData(data) {
    console.log("Received data:", data);
    const scrapedDataContainer = document.getElementById("scrapedDataContainer");

    // Clear previous data
    scrapedDataContainer.innerHTML = "";

    if (data.error) {
        // Display error message
        scrapedDataContainer.innerHTML = `<p>${data.error}</p>`;
    } else {
        const properties = data.data;

        // Create container for cards
        const cardContainer = document.createElement("div");
        cardContainer.classList.add("card-container");

        // Create a card for each property
        properties.data.forEach((property) => {
            const card = document.createElement("div");
            card.classList.add("property-card");

            // Display property details in the card
            for (let i = 0; i < property.length; i++) {
                const cardItem = document.createElement("div");
                cardItem.classList.add("card-item");

                // Handle image URLs
                if (properties.columns[i] === "Image_URL") {
                    if (Array.isArray(property[i])) {
                        const imageContainer = document.createElement("div");
                        imageContainer.classList.add("image-container");

                        property[i].forEach((imageUrl) => {
                            const image = document.createElement("img");
                            image.src = imageUrl;
                            imageContainer.appendChild(image);
                        });

                        cardItem.appendChild(imageContainer);
                    } else {
                        const image = document.createElement("img");
                        image.src = property[i];
                        cardItem.appendChild(image);
                    }
                } else {
                    // Handle non-image content
                    cardItem.innerHTML = `<strong>${properties.columns[i]}:</strong> ${decodeEntities(property[i])}`;
                }

                card.appendChild(cardItem);
            }

            // Add "Get Location" button
            const getLocationButton = document.createElement("button");
            getLocationButton.textContent = "Get Location";
            getLocationButton.addEventListener("click", () => {
                // Modify this function to fetch and display location data
                getLocation(property[properties.columns.indexOf("Title")], property[properties.columns.indexOf("City_name")]);
            });

            card.appendChild(getLocationButton);

            cardContainer.appendChild(card);
        });

        scrapedDataContainer.appendChild(cardContainer);
    }
}

// Modified getLocation function to open Google Maps in a new window
function getLocation(title, city) {
    // Modify this function to fetch and display location data
    console.log("Getting location for:", title, city);

    // Construct Google Maps search query
    const searchQuery = `${title} ${city}`;
    const googleMapsUrl = `https://www.google.com/maps?q=${encodeURIComponent(searchQuery)}`;

    // Open Google Maps in a new window
    window.open(googleMapsUrl, '_blank');
}

function decodeEntities(text) {
  const element = document.createElement("div");
  element.innerHTML = text;
  return element.textContent;
}

// Add some CSS styles for the cards
const style = document.createElement("style");
style.innerHTML = `
.card-container {
    height: 1000px;
    width: 50%;
    overflow-x: auto;
    margin-right: 20px;
    margin-left: auto;
    margin-right: auto;
}


  .property-card {
    display: flex;
    flex-direction: column; /* Display cards in a single column */
    gap: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #fff;
    width: 100%; /* Adjust the width as needed */
    margin-bottom: 20px; /* Add margin between cards */
  }

  .card-item {
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }

  .image-container {
    display: flex;
    justify-content: flex-start; /* Align images from the start */
    overflow-x: auto; /* Enable horizontal scrolling for images */
  }

  .image-container img {
  .image-container img {
    max-width: 100%;
    max-height: 600px; /* Adjust the max height as needed */
    object-fit: cover;
    margin-right: 10px; /* Add margin between images */
  }
`;

document.head.appendChild(style);
