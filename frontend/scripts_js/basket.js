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
    const products = await fetchProducts();
    const basket = await getBasketItems();
    await fillTable(products, basket);
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

async function getBasketItems() {
    return JSON.parse(localStorage.getItem('basket')) || [];
}

async function fillTable(products, basket) {
    const table = document.querySelector('#basket-table tbody');
    const totalPriceElem = document.getElementById('total-price');
    let totalPrice = 0;

    for (let i = 1; i <= basket.length; i++) {
        const product = products.find((p) => {return p.id === basket[i - 1]});
        totalPrice += product.price;
        await pushToTable(table, i, product);
    }
    totalPriceElem.textContent = `${formatPrice(totalPrice)} ₽`
}

async function pushToTable(table, number, product) {
    let newRow = table.insertRow();

    let numCell = newRow.insertCell();
    let numText = document.createTextNode(number);
    numCell.appendChild(numText);

    let titleCell = newRow.insertCell();
    let titleText = document.createTextNode(product.title);
    titleCell.appendChild(titleText);

    let imgCell = newRow.insertCell();
    imgCell.classList.add('product-image');
    let imgContent = document.createElement('img');
    imgContent.src = product.image_url;
    imgCell.appendChild(imgContent);

    let typeCell = newRow.insertCell();
    let typeText = document.createTextNode(productTypes[product.product_type]);
    typeCell.appendChild(typeText);

    let priceCell = newRow.insertCell();
    let priceText = document.createTextNode(`${formatPrice(product.price)} ₽`);
    priceCell.appendChild(priceText);

    let actionsCell = newRow.insertCell();
    const actionsDiv = document.createElement('div');
    actionsDiv.classList.add('actions');

    const deleteButton = document.createElement('button');
    const handleDeleteClick = () => removeFromBasket(product.id);
    deleteButton.addEventListener('click', handleDeleteClick);
    const deleteImg = document.createElement('img');
    deleteImg.src = 'assets/icons/delete.svg';
    deleteButton.appendChild(deleteImg);

    actionsDiv.appendChild(deleteButton);
    
    actionsCell.appendChild(actionsDiv);
}

async function removeFromBasket(id) {
    let basket = JSON.parse(localStorage.getItem('basket')) || [];
  
    if (basket.indexOf(id) !== -1) {
        basket.splice(basket.indexOf(id), 1);
        localStorage.setItem('basket', JSON.stringify(basket));
        location.reload();
    } else {
        console.log(`Товар с ID ${id} не найден в корзине.`);
    }
}

function formatPrice(price) {
    return String(price).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$& ')
}
