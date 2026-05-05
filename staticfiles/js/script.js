
function addToCart(id, name, price) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push({id, name, price});
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(name + " savatga qo'shildi!");
    updateCartCount();
}

function updateCartCount() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let countElement = document.getElementById('cart-count');
    if (countElement) countElement.innerText = cart.length;
}

document.addEventListener('DOMContentLoaded', updateCartCount);
// Savatni yuklash
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(id, name, price) {
    const product = { id, name, price };
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    
    updateCartCount();
    alert(name + " savatga qo'shildi!");
}

function updateCartCount() {
    const badge = document.getElementById('cart-count');
    if (badge) badge.innerText = cart.length;
}

// Sahifa yuklanganda sonini yangilash
document.addEventListener('DOMContentLoaded', updateCartCount);
function updateCartCount() {
    // 1. HTML-dagi sonni ko'rsatuvchi elementni topamiz 🔍
    const cartCountElement = document.getElementById('cart-count');
    
    if (cartCountElement) {
        // 2. Savatdagi mahsulotlar sonini elementga yozamiz ✍️
        cartCountElement.innerText = cart.length;
    }
}