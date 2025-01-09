const productTypes = {
    'electric-guitar': 'Электрогитара',
    'acoustic-guitar': 'Акустическая гитара',
    'drum': 'Ударные',
    'digital-piano': 'Цифровое пианино',
    'acoustic-piano': 'Акустическое пианино',
    'microphone': 'Микрофон',
    'headphone': 'Наушники',
    'sound-system': 'Звуковая система',
    'sound-card': 'Звуковая карта',
    'combo-amplifier': 'Комбоусилитель',
    'mediator': 'Медиатор',
    'string': 'Струны',
    'drumstick': 'Барабанные палочки',
    'cover': 'Чехол',
    'chair': 'Стул',
}

document.addEventListener('DOMContentLoaded', async function () {
    products = await fetchProducts();
    await populateCards(products);
});


async function fetchProducts() {
    const response = await fetch('http://localhost:8000/api/product/all');
    if (response.status === 200) {
        data = response.json();
        return data;
    } else {
        console.log('Ошибка при загрузке товаров')
    }
}

async function populateCards(products) {
    products.forEach(async (product) => {
        const container = document.getElementById(`${product.product_type}s`);
        const card = await createCard(product);
        container.appendChild(card);
    })
}

async function createCard(product) {
    const card = document.createElement('div');
    card.classList.add('card');
    
    const img = document.createElement('img');
    img.src = product.image_url;
    const handleCardClick = () => goToProduct(product);
    img.addEventListener('click', handleCardClick);
    card.appendChild(img);

    const price = document.createElement('p');
    price.textContent = `${formatPrice(product.price)} ₽`;
    card.appendChild(price);

    const productType = document.createElement('p');
    productType.textContent = productTypes[product.product_type];
    card.appendChild(productType);

    const title = document.createElement('h2');
    title.textContent = product.title;
    card.appendChild(title);

    const button = document.createElement('button');
    const handleProductClick = () => addToBasket(product);
    button.addEventListener('click', handleProductClick);
    button.textContent = 'Добавить';
    card.appendChild(button);

    return card;
}

async function addToBasket (product) {
    if (!window.localStorage.getItem('user-email')) {
        displayNotification('Для сохранения товаров в корзину требуется авторизоваться');
        return;
    }

    let basket = JSON.parse(localStorage.getItem('basket')) || [];

    if (!basket.includes(product.id)) {
        basket.push(product.id);
        localStorage.setItem('basket', JSON.stringify(basket));
        displayNotification('Товар добавлен в корзину');
    }
}

async function getBasketItems() {
    return JSON.parse(localStorage.getItem('basket')) || [];
}

function goToProduct(product) {
    location.assign(`product.html?id=${product.id}`);
}

function formatPrice(price) {
    return String(price).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$& ')
}

function displayNotification(message) {
    const notification = document.getElementById('notification');
    notification.style.opacity = '1';

    const notificationMessage = document.createElement('p');
    notificationMessage.textContent = message
    notification.appendChild(notificationMessage);

    const notificationButton = document.createElement('button');
    notificationButton.innerHTML = 'Окей <span>&#128076;</span>';
    notificationButton.addEventListener('click', function () {
        const notification = document.getElementById('notification');
        notification.innerHTML = '';
        notification.style.opacity = '0';
    });
    notification.appendChild(notificationButton);
}
