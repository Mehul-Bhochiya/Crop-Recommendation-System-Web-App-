document.addEventListener("DOMContentLoaded", function () {
    const crops = [
        "Wheat", "Rice", "Maize", "Barley",
        "Sugarcane", "Cotton", "Soyabean", "Groundnut",
        "Sunflower", "Pulses", "Millets", "Chickpea",
        "Lentil", "Mustard", "Jute", "Tobacco",
        "Potato", "Tomato", "Onion", "Carrot",
        "Cabbage", "Spinach"
    ];

    const cropList = document.getElementById("cropList");

    const cropGrid = document.createElement("div");
    cropGrid.className = "crop-list";

    crops.forEach(crop => {
        const cropItem = document.createElement("div");
        cropItem.className = "crop-item";
        cropItem.textContent = crop;
        cropItem.addEventListener("click", function () {
            window.location.href = `crops/${crop.toLowerCase()}.html`;
        });
        cropGrid.appendChild(cropItem);
    });

    const cropMenuItem = document.createElement("li");
    cropMenuItem.appendChild(cropGrid);
    cropList.appendChild(cropMenuItem);
});
