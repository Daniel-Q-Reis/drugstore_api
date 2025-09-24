// A signal to check if the script is loaded at all.
console.log("Sales Admin Script: Loaded successfully.");

document.addEventListener('DOMContentLoaded', () => {
    // This function will execute once the entire HTML document is ready.
    console.log("Sales Admin Script: DOM is ready.");

    const stockDataElement = document.getElementById('stock_items_json');
    if (!stockDataElement) {
        console.error('CRITICAL ERROR: The <script id="stock_items_json"> tag was not found.');
        return;
    }
    const stockData = JSON.parse(stockDataElement.textContent);
    console.log("Sales Admin Script: Stock data parsed.");

    function updateRowCalculations(row) {
        const stockItemSelect = row.querySelector('select[id$="-stock_item"]');
        const quantityInput = row.querySelector('input[id$="-quantity"]');
        const unitPriceInput = row.querySelector('input[id$="-unit_price"]');
        const discountInput = row.querySelector('input[id$="-discount_percentage"]');
        const totalPriceInput = row.querySelector('input[id$="-total_price"]');

        if (!stockItemSelect || !quantityInput) return;

        const selectedStockId = stockItemSelect.value;
        const itemData = stockData[selectedStockId];
        let quantity = parseInt(quantityInput.value, 10) || 0;

        if (itemData) {
            if (quantity > itemData.quantity) {
                quantityInput.style.backgroundColor = '#ffdddd';
            } else {
                quantityInput.style.backgroundColor = '';
            }

            const sellingPrice = parseFloat(itemData.selling_price);
            const discountPercentage = parseFloat(itemData.discount_percentage);
            const discountMultiplier = 1 - (discountPercentage / 100);
            const discountedUnitPrice = sellingPrice * discountMultiplier;

            unitPriceInput.value = discountedUnitPrice.toFixed(2);
            discountInput.value = discountPercentage.toFixed(2);
            totalPriceInput.value = (discountedUnitPrice * quantity).toFixed(2);
        } else {
            unitPriceInput.value = '';
            discountInput.value = '';
            totalPriceInput.value = '';
        }
        updateGrandTotals();
    }

    function updateGrandTotals() {
        const totalAmountInput = document.querySelector("#id_total_amount");
        const discountAmountInput = document.querySelector("#id_discount_amount");
        const finalAmountInput = document.querySelector("#id_final_amount");

        let totalGross = 0;
        let totalDiscount = 0;

        document.querySelectorAll('#items-group .form-row').forEach(row => { // CORRECTED CLASS
            const stockItemSelect = row.querySelector('select[id$="-stock_item"]');
            const quantityInput = row.querySelector('input[id$="-quantity"]');
            
            if (stockItemSelect && quantityInput) {
                const selectedStockId = stockItemSelect.value;
                const quantity = parseInt(quantityInput.value, 10) || 0;
                const itemData = stockData[selectedStockId];

                if (itemData) {
                    const sellingPrice = parseFloat(itemData.selling_price);
                    const discountPercentage = parseFloat(itemData.discount_percentage);
                    const grossRowPrice = sellingPrice * quantity;
                    const discountRowValue = grossRowPrice * (discountPercentage / 100);

                    totalGross += grossRowPrice;
                    totalDiscount += discountRowValue;
                }
            }
        });

        totalAmountInput.value = totalGross.toFixed(2);
        discountAmountInput.value = totalDiscount.toFixed(2);
        finalAmountInput.value = (totalGross - totalDiscount).toFixed(2);
    }

    function initializeRow(row) {
        console.log("Sales Admin Script: Initializing new or existing row.", row);
        const stockItemSelect = row.querySelector('select[id$="-stock_item"]');
        const quantityInput = row.querySelector('input[id$="-quantity"]');

        if (stockItemSelect) {
            stockItemSelect.addEventListener('change', () => {
                if (parseInt(quantityInput.value, 10) === 0 || !quantityInput.value) {
                    quantityInput.value = 1;
                }
                updateRowCalculations(row);
            });
        }
        if (quantityInput) {
            quantityInput.addEventListener('input', () => {
                updateRowCalculations(row);
            });
        }

        if (stockItemSelect && stockItemSelect.value) {
            updateRowCalculations(row);
        }
    }

    const inlineContainer = document.getElementById('items-group');
    if (inlineContainer) {
        console.log("Sales Admin Script: Found inline container with ID 'items-group'. Success!");
        
        inlineContainer.querySelectorAll('.form-row').forEach(initializeRow); // CORRECTED CLASS

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList.contains('form-row')) { // CORRECTED CLASS
                        initializeRow(node);
                    }
                });
            });
        });
        observer.observe(inlineContainer, { childList: true, subtree: true });
    } else {
        console.warn("Sales Admin Script: CRITICAL - Could not find inline container.");
    }
});