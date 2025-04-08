document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.getElementById('editButton');
    const saveButton = document.getElementById('saveButton');
    const cancelButton = document.getElementById('cancelButton');
    const editControls = document.getElementById('editControls');
    const inputFields = document.querySelectorAll('.input-field');

    // Rental Details Tabs
    const currentRentalsBtn = document.getElementById('currentRentalsBtn');
    const pastRentalsBtn = document.getElementById('pastRentalsBtn');
    const currentRentalsList = document.getElementById('currentRentalsList');
    const pastRentalsList = document.getElementById('pastRentalsList');
    const accountTab = document.getElementById('accountTab');
    const rentedVehicleTab = document.getElementById('rentedVehicleTab');
    const tabContents = document.querySelectorAll('.tab-content');
    const tabButtons = document.querySelectorAll('.tab-button');
    function showTab(tabId) {
        tabContents.forEach(tab => tab.classList.add('hidden'));
        tabButtons.forEach(button => button.classList.remove('active'));
        document.getElementById(tabId).classList.remove('hidden');
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    }
    function showCurrentRentals() {
        currentRentalsList.classList.remove('hidden');
        pastRentalsList.classList.add('hidden');
        currentRentalsBtn.classList.add('active');
        pastRentalsBtn.classList.remove('active');
    }
    function showPastRentals() {
        pastRentalsList.classList.remove('hidden');
        currentRentalsList.classList.add('hidden');
        pastRentalsBtn.classList.add('active');
        currentRentalsBtn.classList.remove('active');
    }
    currentRentalsBtn.addEventListener('click', showCurrentRentals);
    pastRentalsBtn.addEventListener('click', showPastRentals);

    function enableEdit() {
        inputFields.forEach(input => {
            input.disabled = false;
            input.classList.remove('input-field:disabled');
            input.focus();
        });
        editButton.style.display = 'none';
        editControls.style.display = 'block';
    }
    function disableEdit() {
        inputFields.forEach(input => {
            input.disabled = true;
            input.classList.add('input-field:disabled');
        });
        editButton.style.display = 'block';
        editControls.style.display = 'none';
    }
    //Setup button click
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            showTab(tabId);
        });
    });
    accountTab.addEventListener('click', () => {
        showTab('accountDetails');
    });
    rentedVehicleTab.addEventListener('click', () => {
        showTab('rentedVehicleDetails');
    });
    editButton.addEventListener('click', enableEdit);
    cancelButton.addEventListener('click', disableEdit);
    //Show correct content on load
    if (window.location.hash === '#rentedVehicleDetails') {
        showTab('rentedVehicleDetails');
    } else {
        showTab('accountDetails'); // Default to account if no hash
    }

});
