document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const chatbotIcon = document.getElementById('chatbot-icon');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatLog = document.getElementById('chat-log');
    const loginSignupPopup = document.getElementById('loginSignupPopup');
    const wrapper = document.querySelector('.wrapper');
    const signUpLink = document.querySelector('.link .signup-link');
    const signInLink = document.querySelector('.link .signin-link');

    // Function to toggle chatbot visibility
    window.toggleChatbot = function () {
        if (chatbotWindow.style.display === 'none') {
            chatbotWindow.style.display = 'block'; // Show
            if (chatLog.innerHTML === "") {
                introduceBot(); // Initialize if chat log is empty
            }
        } else {
            chatbotWindow.style.display = 'none'; // Hide
        }
    };

    // Function to toggle login/signup popup visibility
    window.toggleLoginSignup = function () {
        loginSignupPopup.style.display = loginSignupPopup.style.display === 'none' ? 'flex' : 'none';
        if (loginSignupPopup.style.display === 'flex') {
            wrapper.classList.remove('animated-signup'); // Ensure login is shown by default
            wrapper.classList.add('animated-signin');
        }
    };


    // Corrected function to introduce bot messages
    function introduceBot() {
        const introduction = "Hello! How can I help you today?";
        appendMessage('Chatbot', introduction, 'chatbot-message');

        const optionsData = [
            { text: "Account", response: "For account-related queries, you can manage your profile, view booking history, and update your details. What would you like to do?" },
            { text: "Vehicle", response: "Looking for vehicles? We offer Cycles, Bikes, Cars, and Trucks. Tell me what type you're interested in." },
            { text: "How to book", response: "Booking is easy! Simply select your desired vehicle type, choose your rental dates and times, and proceed to checkout." },
            { text: "Rental policies", response: "Our rental policies cover aspects like duration, mileage, security deposits, and cancellations. Which specific policy are you interested in?" },
            { text: "Booking confirmation", response: "Once your booking is complete, you'll receive a confirmation email with all the details. Have you made a booking already?" },
            { text: "Contact support", response: "Need to contact our support team? You can reach us via email at support@drivewheelz.com or call us at +91 [Phone Number]. How else can we assist you?" }
        ];

        const optionsContainer = document.createElement('div');
        optionsContainer.classList.add('chatbot-options-container');

        optionsData.forEach(optionData => {
            const optionButton = document.createElement('button');
            optionButton.textContent = optionData.text;
            optionButton.classList.add('chatbot-option-button');

            optionButton.onclick = function () {
                const userQuery = optionData.text;
                appendMessage('You', userQuery, 'user'); // Append user message

                // Find and close any currently open response
                const allResponseDivs = document.querySelectorAll('.chatbot-response-content');
                allResponseDivs.forEach(div => div.style.display = 'none');

                const responseText = optionData.response;
                appendMessage('Chatbot', responseText, 'chatbot-message'); // Append bot response
            };
            optionsContainer.appendChild(optionButton);
        });

        chatLog.appendChild(optionsContainer);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Fetch API to respond with a message from the chatbot
    function handleUserQuery(query) {
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(query)}`,
        })
            .then(response => response.json())
            .then(data => {
                appendMessage('Chatbot', data.response, 'chatbot-message');
            })
            .catch(error => console.error('Fetch error:', error));
    }

    // Added to generate new chat messages.
    function appendMessage(sender, text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = className;
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    if (signUpLink && signInLink && wrapper) {
        signUpLink.addEventListener('click', (e) => {
            e.preventDefault();
            wrapper.classList.add('animated-signup'); // Show signup
            wrapper.classList.remove('animated-signin'); // Hide login
        });

        signInLink.addEventListener('click', (e) => {
            e.preventDefault();
            wrapper.classList.add('animated-signin'); // Show login
            wrapper.classList.remove('animated-signup'); // Hide signup
        });
    }

    // You could have style changes in this section
    document.getElementById('bg').style.backgroundColor = '#f4f4f4';
    document.getElementById('bg').style.color = '#333';
});

function showNotLoggedInAlert() {
    alert("Please log in to access your profile.");
}

document.addEventListener('DOMContentLoaded', () => {
    const interBubble = document.querySelector('.interactive');
    let curX = 0;
    let curY = 0;
    let tgX = 0;
    let tgY = 0;

    function move() {
        curX += (tgX - curX) / 20;
        curY += (tgY - curY) / 20;
        interBubble.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
        requestAnimationFrame(move);
    }

    window.addEventListener('mousemove', (event) => {
        tgX = event.clientX;
        tgY = event.clientY;
    });

    move();
});