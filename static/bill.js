document.addEventListener('DOMContentLoaded', () => {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const profileBtn = document.querySelector('.profile-btn');
    const dropdownContent = document.querySelector('.profile-dropdown-content');

    if (profileDropdown && profileBtn && dropdownContent) {
        profileBtn.addEventListener('click', () => {
            dropdownContent.style.display = (dropdownContent.style.display === 'block' || dropdownContent.style.display === '') ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        window.addEventListener('click', (event) => {
            if (!profileDropdown.contains(event.target)) {
                dropdownContent.style.display = 'none';
            }
        });
    }
});