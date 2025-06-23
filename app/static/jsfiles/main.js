// Searching Bar Making at FQAs
// const searchInput = document.getElementById('faqSearch');
// const searchButton = document.getElementById('searchButton');
// const accordionItems = document.querySelectorAll('.searchable');
// const noResultsMessage = document.getElementById('noResults');

// function performSearch() {
//     const searchTerm = searchInput.value.toLowerCase();
//     let visibleItems = 0;

//     accordionItems.forEach(item => {
//         const question = item.querySelector('.accordion-button').textContent.toLowerCase();
//         const answer = item.querySelector('.accordion-body').textContent.toLowerCase();
//         const isVisible = question.includes(searchTerm) || answer.includes(searchTerm);
        
//         item.style.display = isVisible ? 'block' : 'none';
//         if (isVisible) visibleItems++;

//         // Collapse all items initially
//         const collapse = item.querySelector('.accordion-collapse');
//         if (!isVisible && collapse.classList.contains('show')) {
//             bootstrap.Collapse.getInstance(collapse)?.hide();
//         }
//     });

//     noResultsMessage.classList.toggle('d-none', visibleItems > 0);
// }

// // Event listeners
// searchInput.addEventListener('input', performSearch);
// searchButton.addEventListener('click', performSearch);
// document.getElementById('searchForm').addEventListener('submit', (e) => {
//     e.preventDefault();
//     performSearch();
// });

// Contact Us Form Sending Via What'sapp
function sendMessage(event) {
    event.preventDefault();

    const phoneInput = document.getElementById('phone').value.trim();
    const name = document.getElementById('name').value.trim();
    const messageText = document.getElementById('message').value.trim();

    if (phoneInput && name && messageText) {
        const fullMessage = 
            `مرحبًا، لدي رسالة من النموذج:\n\n` +
            `الاسم: ${name}\n` +
            `رقم التواصل: ${phoneInput}\n` +
            `الرسالة: ${messageText}`;
        
        const encodedMessage = encodeURIComponent(fullMessage);
        const whatsappURL = `https://wa.me/+201118954564?text=${encodedMessage}`;

        window.open(whatsappURL, '_blank');
    }
}