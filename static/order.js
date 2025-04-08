const vehicleData = {
    car: {
        brands: {
            Tata: {
                name: 'Tata',
                description: 'Leading Indian automobile manufacturer known for its affordable and reliable cars.',
                image: 'tata_logo.png',
                models: [
                    { name: 'Tata Tiago', image: 'TC1.png' },
                    { name: 'Tata Punch', image: 'TC2.png' },
                    { name: 'Tata Nexon', image: 'TC3.png' }
                ]
            },
            Marutisuzuki: {
                name: 'Maruti Suzuki',
                description: 'India\'s largest passenger car maker, offering a wide range of fuel-efficient vehicles.',
                image: 'maruti_logo.png',
                models: [
                    { name: 'Swift', image: 'MSC1.png' },
                    { name: 'Grand Vitara', image: 'MSC2.png' },
                    { name: 'JIMNY', image: 'MSC3.png' }
                ]
            },
            Mahindra: {
                name: 'Mahindra',
                description: 'Indian multinational automotive company specializing in utility vehicles and SUVs.',
                image: 'mahindra_logo.png',
                models: [
                    { name: 'XUV 700', image: 'MC1.png' },
                    { name: 'THAR ROXX', image: 'MC2.png' },
                    { name: 'Scorpio Classic', image: 'MC3.png' }
                ]
            }
        }
    },
    bike: {
        brands: {
            Yamaha: {
                name: 'Yamaha',
                description: 'Japanese manufacturer renowned for its high-performance motorcycles and scooters.',
                image: 'yamaha_logo.png',
                models: [
                    { name: 'Fascino 125 Fi', image: 'YB1.PNG' },
                    { name: 'R15(v4)', image: 'YB2.png' },
                    { name: 'MATTE COPPER', image: 'YB3.png' }
                ]
            },
            Bajaj: {
                name: 'Bajaj',
                description: 'Indian multinational motorcycle manufacturer, known for its diverse range of bikes and scooters.',
                image: 'bajaj_logo4.png',
                models: [
                    { name: 'Bajaj CT 110X', image: 'BB1.png' },
                    { name: 'Bajaj Pulsar NS200', image: 'BB2.png' },
                    { name: 'Bajaj Avenger 220 Cruise', image: 'BB3.png' }
                ]
            },
            RoyalEnfield: {
                name: 'Royal Enfield',
                description: 'Classic British motorcycle brand now made in India, famous for its retro styling and touring capabilities.',
                image: 'royalenfield_logo.png',
                models: [
                    { name: 'Classic 350', image: 'REB1.png' },
                    { name: 'Himalayan 450', image: 'REB2.png' },
                    { name: 'Bullet 350', image: 'REB3.png' }
                ]
            }
        }
    },
    cycle: {
        brands: {
            Hercules: {
                name: 'Hercules',
                description: 'Popular Indian bicycle brand offering a variety of models for different needs.',
                image: 'hercules_logo.png',
                models: [
                    { name: 'Hercules FX100', image: 'HC1.png' },
                    { name: 'Hercules Roadeo Fugitive SS', image: 'HC2.png' },
                    { name: 'Hercules hard style', image: 'HC3.png' }
                ]
            },
            Hero: {
                name: 'Hero',
                description: 'One of the largest bicycle manufacturers in the world, with a wide range of affordable and reliable cycles.',
                image: 'herocycles_logo.png',
                models: [
                    { name: 'Hero New Attitude', image: '/HEC1.png' },
                    { name: 'Hero Trot', image: 'HEC2.png' },
                    { name: 'Hero Lectro H7+', image: 'HEC3.png' }
                ]
            },
            Avon: {
                name: 'Avon',
                description: 'Indian bicycle manufacturer known for its innovative designs and quality products.',
                image: 'avoncycles_logo.png',
                models: [
                    { name: 'CYCLUX SAGE', image: '/AC1.png' },
                    { name: 'AHEAD 700 x 35C', image: 'AC2.png' },
                    { name: 'CYCLELEC CONNECT PRO', image: 'AC3.png' }
                ]
            }
        }
    },
    truck: {
        brands: {
            Tata: {
                name: 'Tata',
                description: 'India\'s largest commercial vehicle manufacturer, offering a comprehensive range of trucks for various applications.',
                image: 'tata_logo.png',
                models: [
                    { name: 'TATA SFC 712', image: 'TT1.JPG' },
                    { name: 'TATA SIGNA 1923.K', image: 'TT2.JPG' },
                    { name: 'TATA SIGNA 4021.S', image: 'TT3.JPG' }
                ]
            },
            AshokLeyland: {
                name: 'Ashok Leyland',
                description: 'Indian automobile manufacturer and a leading maker of trucks and buses.',
                image: 'ashokleyland_logo.png',
                models: [
                    { name: 'Haulage 8x2(gvw : 35t)', image: 'ALT1.png' },
                    { name: 'Tipper 10x4', image: 'ALT2.png' },
                    { name: 'ICVTipper', image: 'ALT3.png' }
                ]
            },
            BharatBenz: {
                name: 'Bharat Benz',
                description: 'Indian commercial vehicle manufacturer that is a division of Daimler Truck AG.',
                image: 'bharatbenz_logo.jpg',
                models: [
                    { name: 'Medium Duty Trucks', image: 'BBT1.png' },
                    { name: 'Heavy Duty Tractors', image: 'BBT2.png' },
                    { name: 'Heavy Duty Rigid Tippers', image: 'BBT3.png' }
                ]
            }
        }
    }
};

const brandNameMap = {
    Marutisuzuki: 'Maruti suzuki',
    RoyalEnfield: 'Royal Enfield',
    AshokLeyland: 'Ashok leyland',
    BharatBenz: 'Bharat benz',
    Mahindra: 'Mahindra',
    Tata: 'Tata',
    Yamaha: 'Yamaha',
    Bajaj: 'Bajaj',
    Hero: 'Hero',
    Hercules: 'Hercules',
    Avon: 'Avon'
};

let selectedVehicle = null;
let selectedBrand = null;
let selectedModel = null;

// Vehicle Type Selection
document.querySelectorAll('.vehicle-card').forEach(card => {
    const type = card.dataset.type;
    const details = {
        cycle: { title: 'Cycle Details', specs: ['Type: Road/Mountain', 'Gears: 7-21 Speed', 'Top Brands: Trek, Cannondale'] },
        bike: { title: 'Bike Details', specs: ['Engine: 150-500cc', 'Mileage: 30-50 kmpl', 'Top Brands: Harley, Ducati'] },
        car: { title: 'Car Details', specs: ['Seats: 4-5', 'Mileage: 12-18 kmpl', 'Top Brands: Mercedes, BMW'] },
        truck: { title: 'Truck Details', specs: ['Capacity: 1-5 Tons', 'Engine: Diesel', 'Top Brands: Ford, Toyota'] },
    };
    const detail = details[type];
    if (detail) {
        const popup = card.querySelector('.popup');
        if (!popup) {
            const popupContent = document.createElement('div');
            popupContent.className = 'popup';
            popupContent.innerHTML = `
                <div class="popup-content">
                    <h4>${detail.title}</h4>
                    ${detail.specs.map(spec => `<p>${spec}</p>`).join('')}
                </div>
            `;
            card.appendChild(popupContent);
        }
    }
    card.addEventListener('click', () => {
        selectedVehicle = card.dataset.type;
        showSection('#brandSection');
        populateBrands();
    });
});

function populateBrands() {
    const brandCards = document.getElementById('brandCards');
    brandCards.innerHTML = '';

    Object.keys(vehicleData[selectedVehicle].brands).forEach(brandKey => {
        const brand = vehicleData[selectedVehicle].brands[brandKey];
        const displayBrand = brandNameMap[brandKey] || brandKey;

        const card = document.createElement('div');
        card.className = 'brand-card';
        card.innerHTML = `
            <img src="/static/images/${brand.image}" alt="${displayBrand}">
            <h3>${displayBrand}</h3>
            <div class="brand-popup">
                <div class="popup-content">
                    <h4>${displayBrand} Details</h4>
                    <p>${brand.description}</p>
                    <p>Type: ${selectedVehicle}</p>
                    <p>Models: ${brand.models.map(m => m.name).join(', ')}</p>
                    <p>Service: Nationwide</p>
                    <p>Warranty: 1-3 Years</p>
                </div>
            </div>
        `;
        card.addEventListener('click', () => {
            selectedBrand = brandKey;
            showSection('#modelSection');
            populateModels();
        });
        brandCards.appendChild(card);
    });
}

function populateModels() {
    const modelCards = document.getElementById('modelCards');
    modelCards.innerHTML = '';

    const models = vehicleData[selectedVehicle].brands[selectedBrand].models;

    models.forEach(model => {
        const card = document.createElement('div');
        card.className = 'model-card';
        card.innerHTML = `
            <img src="/static/images/${model.image}" alt="${model.name}">
            <h3>${model.name}</h3>
            <div class="model-popup">
                <div class="popup-content">
                    <h4>${model.name} Specs</h4>
                    <p>Engine: 1.2L-2.0L</p>
                    <p>Mileage: 15-25 kmpl</p>
                    <p>Seating: 2-5 Persons</p>
                    <p>Fuel: Petrol/Diesel</p>
                    <p>Description: Specific details about the ${model.name} will be available upon selection.</p>
                </div>
            </div>
            <div class="image-popup">
                <img src="/static/images/${model.image}" alt="${model.name}">
            </div>
        `;
        card.addEventListener('click', () => {
            selectedModel = model.name;
            showSection('#dateSection');
            setupDatePicker();
            document.getElementById('rentButton').classList.remove('hidden');
        });
        modelCards.appendChild(card);
    });
}

function setupDatePicker() {
    const today = new Date().toISOString().split('T')[0];
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');

    startDateInput.min = today;
    endDateInput.min = today;

    startDateInput.addEventListener('change', () => {
        endDateInput.min = startDateInput.value;
        if (new Date(endDateInput.value) < new Date(startDateInput.value)) {
            endDateInput.value = startDateInput.value;
        }
    });
}

document.getElementById('rentNowBtn').addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default form submission

    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    if (!startDate || !endDate) {
        alert('Please select both dates.');
        return;
    }

    const days = Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24)) || 1;

    const formData = new FormData();
    formData.append('vehicle_type', selectedVehicle);
    formData.append('brand', brandNameMap[selectedBrand] || selectedBrand);
    formData.append('model', selectedModel);
    formData.append('start_date', startDate);
    formData.append('end_date', endDate);
    formData.append('days', days);

    fetch('/bill', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/bill';
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (typeof data === 'object' && data.error) {
            alert(data.error + (data.next_available_date ? ` Next available date: ${data.next_available_date}` : ''));
            startDateInput.value = '';
            endDateInput.value = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during the booking process.');
    });
});

function showSection(sectionId) {
    const section = document.querySelector(sectionId);
    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('mouseover', (e) => {
    if (e.target.closest('.vehicle-card, .brand-card, .model-card')) {
        e.target.closest('.vehicle-card, .brand-card, .model-card').classList.add('hover-active');
    }
});

document.addEventListener('mouseout', (e) => {
    if (e.target.closest('.vehicle-card, .brand-card, .model-card')) {
        e.target.closest('.vehicle-card, .brand-card, .model-card').classList.remove('hover-active');
    }
});