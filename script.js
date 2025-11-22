// --- Data and Storage ---
const products = [
    { id: 1, name: 'Fresh Red Apples', price: 2.99, category: 'Fruits', image: 'https://via.placeholder.com/150x120?text=Apples' },
    { id: 2, name: 'Organic Carrots', price: 1.50, category: 'Vegetables', image: 'https://via.placeholder.com/150x120?text=Carrots' },
    { id: 3, name: 'Whole Milk', price: 4.50, category: 'Groceries', image: 'https://via.placeholder.com/150x120?text=Milk' },
]; // Assuming product data is here
const CART_STORAGE_KEY = 'grocifyCart';
const AUTH_TOKEN_KEY = 'auth_token';
const USER_DETAILS_KEY = 'user_details';

let cart = JSON.parse(localStorage.getItem(CART_STORAGE_KEY)) || [];

function saveCart() {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
}

// --- Cart Logic (Simplified) ---
function calculateTotal() {
    return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

function showCart() {
    document.getElementById('cart-modal').style.display = 'block';
    
    const cartItemsList = document.getElementById('cart-items');
    cartItemsList.innerHTML = ''; // Clear previous items

    if (cart.length === 0) {
         cartItemsList.innerHTML = '<li>Your cart is empty.</li>';
    } else {
        // --- NOTE: Add actual cart item rendering logic here ---
        cart.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="cart-item-info">
                    <span>${item.name}</span>
                </div>
                <span>Rs. ${(item.price * item.quantity).toFixed(2)}</span>
            `;
            cartItemsList.appendChild(li);
        });
    }
    document.getElementById('cart-item-count').textContent = cart.length;
    document.getElementById('cart-total-price').textContent = calculateTotal().toFixed(2);
}

function hideCart() {
    document.getElementById('cart-modal').style.display = 'none';
}

// --- NEW FUNCTION: Redirect to Place Order Page ---
window.placeOrder = function() {
    if (cart.length === 0) {
        alert("Your cart is empty. Please add items before placing an order.");
        return;
    }

    const total = calculateTotal();
    
    // Serialize the cart data and total into URL query parameters
    const cartJson = JSON.stringify(cart);
    const totalEncoded = encodeURIComponent(total.toFixed(2));
    const cartEncoded = encodeURIComponent(cartJson);

    // Redirect to the new placeorder page
    window.location.href = `/placeorder.html?cart=${cartEncoded}&total=${totalEncoded}`;
    
    // Crucial: Clear the local cart after successful order initiation (optional: clear on success POST)
    // For now, we clear it *after* the server confirms the order in the POST route.
    // However, if using URL params, it's safer to clear the storage *after* the final server confirmation.
    // We leave the clearing logic to be handled by the Flask POST successful response.
};


// --- Authentication UI Logic (Remains the same) ---
function updateAuthUI() {
    const loginLink = document.getElementById('auth-login');
    const registerLink = document.getElementById('auth-register');
    const logoutBtn = document.getElementById('auth-logout');
    const isLoggedIn = localStorage.getItem(AUTH_TOKEN_KEY);

    if (loginLink && logoutBtn && registerLink) {
        if (isLoggedIn) {
            loginLink.style.display = 'none';
            registerLink.style.display = 'none';
            logoutBtn.style.display = 'list-item'; 
        } else {
            loginLink.style.display = 'list-item'; 
            registerLink.style.display = 'list-item'; 
            logoutBtn.style.display = 'none';
        }
    }
}

window.logout = function() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_DETAILS_KEY);
    // You might also want to clear the cart here if you aren't storing it permanently per user.
    cart = [];
    saveCart(); 
    
    window.location.href = '/login.html'; 
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // Check if we just confirmed an order, then clear cart
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('order_status') === 'confirmed') {
        cart = [];
        saveCart();
    }
    
    updateAuthUI();
    showCart(); // Initial display of the cart count
});