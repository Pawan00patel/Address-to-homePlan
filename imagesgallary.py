# List of image URLs

image_urls = [
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2019/08/27/Project-Photo-22-Mahaveer-Ranches-Bangalore-5037933_750_1000_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2020/03/05/Project-Photo-24-Mahaveer-Ranches-Bangalore-5037933_750_1000_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2019/08/27/Project-Photo-23-Mahaveer-Ranches-Bangalore-5037933_750_1000_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2019/08/27/Project-Photo-22-Mahaveer-Ranches-Bangalore-5037933_750_1000_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/03/09/Project-Photo-44-Mahaveer-Trident-Bangalore-5123377_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2019/08/27/Project-Photo-18-Mahaveer-Ranches-Bangalore-5037933_750_1000_310_462.jpg",
    "https://img.staticmb.com/mbphoto/property/cropped_images/2023/Apr/29/Photo_h300_w450/66827193_8_B_300_450.jpg",
    "https://img.staticmb.com/mbphoto/property/cropped_images/2023/Apr/29/Photo_h300_w450/66827547_11_B_300_450.jpg",
    "https://img.staticmb.com/mbphoto/property/cropped_images/2023/May/02/Photo_h300_w450/66864467_9_B_300_450.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2021/01/05/Project-Photo-1-DS-MAX-Sahara-Bangalore-5223697_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-2-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-4-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-8-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/27/Project-Photo-1-DSR-Highland-Greenz-Bangalore-5333811_505_2000_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/27/Project-Photo-43-DSR-Highland-Greenz-Bangalore-5333811_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/27/Project-Photo-37-DSR-Highland-Greenz-Bangalore-5333811_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/27/Project-Photo-29-DSR-Highland-Greenz-Bangalore-5333811_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-4-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-8-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-2-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/07/28/Project-Photo-6-Bhavisha-Bentley-Goldberg-Phase-II-Bangalore-5416269_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/27/Project-Photo-26-DSR-Highland-Greenz-Bangalore-5333811_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/15/Project-Photo-2-ARS-Signature-Homes-Bangalore-5333415_600_800_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/15/Project-Photo-6-ARS-Signature-Homes-Bangalore-5333415_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/15/Project-Photo-4-ARS-Signature-Homes-Bangalore-5333415_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2023/05/30/Project-Photo-11-Trifecta-Retto-Bangalore-5409519_1200_1600_310_462.jpg",
    "https://img.staticmb.com/mbimages/project/Photo_h310_w462/2022/07/22/Project-Photo-22-Seren",]


# Create an HTML file
with open('image_gallery.html', 'w') as file:
    # Write the HTML structure
    file.write('<html>\n')
    file.write('<head>\n')
    file.write('<title>Image Gallery</title>\n')
    file.write('</head>\n')
    file.write('<body>\n')

    # Add image tags for each URL
    for image_url in image_urls:
        file.write(f'<img src="{image_url}" alt="Image">\n')

    file.write('</body>\n')
    file.write('</html>\n')

print("HTML file 'image_gallery.html' has been created.")

# Note: Make sure to provide all the image URLs in the 'image_urls' list.
