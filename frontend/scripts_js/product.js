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

document.addEventListener('DOMContentLoaded', async () => {
    const product = await fetchProduct();
    await displayProduct(product);
});

async function fetchProduct() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    const response = await fetch(`http://localhost:8000/api/product/id/${productId}`);

    if (response.status === 200) {
        const data = response.json();
        return data;
    } else {
        console.log('Ошибка запроса товара');
        return null;
    }
}

async function displayProduct(product) {
    if (product !== null) {
        const title = document.getElementById('product-title');
        const type = document.getElementById('product-type');
        const img = document.getElementById('product-img');
        const price = document.getElementById('product-price');
        const button = document.getElementById('addButton');
        const quantity = document.getElementById('product-quantity');
        const description = document.getElementById('product-description');
        const characteristics = document.getElementById('product-characteristics');

        document.title = ` MusixShop - ${product.title}`;
        title.textContent = product.title;
        type.textContent = productTypes[product.product_type];
        img.src = product.image_url;
        price.textContent = `${formatPrice(product.price)} ₽`;
        const handleProductClick = () => addToBasket(product);
        button.addEventListener('click', handleProductClick);
        quantity.textContent = product.quantity !== 0 ? `В наличии ${product.quantity} шт.` : 'Нет в наличии';
        description.textContent = product.description;
        
        Object.entries(product.characteristics).forEach(([key, value]) => {
            const characteristicDiv = document.createElement('div');
            
            const keyParagraph = document.createElement('p');
            keyParagraph.textContent = key + ':';
            characteristicDiv.appendChild(keyParagraph);
            
            const valueParagraph = document.createElement('p');
            valueParagraph.textContent = value;
            characteristicDiv.appendChild(valueParagraph);
            
            characteristics.appendChild(characteristicDiv);
        });

    } else {
        const title = document.getElementById('product-title');
        const front = document.getElementById('product-front');
        const info = document.getElementById('product-info');

        document.title = ` MusixShop - Товар не найден`;
        title.textContent = 'Товар не найден';
        front.style.display = 'none';
        info.style.display = 'none';
    }
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
