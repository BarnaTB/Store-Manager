document.getElementById('refresh').addEventListener('click', refreshTable)
document.getElementById('submit-btn').addEventListener('click', sell)

const url = 'http://localhost:5000/api/v1/products'
var token = localStorage.getItem('token')

let table = document.querySelector('#table')
let center = document.querySelector('.center')
let close = document.querySelector('#close')
let button = document.querySelector('button')

table.onclick = (event) => {
    let td = event.target.closest('td')

    if (event.target.matches('button')) {
        center.style.display = 'block'
        button.style.display = 'none'
    }else if (event.target.matches('#close')) {
        center.style.display = 'none'
        button.style.display = 'block'
    }
}

function refreshTable(event) {
    event.preventDefault()
    let invalid = document.getElementById('invalid')
    let tableBody = document.querySelector('#table > tbody')

    fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === 'Products Fetched!') {
                for (let product of data.products) {
                    newRow = document.createElement('tr')
                    productId = document.createElement('td')
                    productId.textContent = product._id
                    productCategory = document.createElement('td')
                    productCategory.innerHTML = product.category
                    productName = document.createElement('td')
                    productName.innerHTML = product.name
                    productQuantity = document.createElement('td')
                    productQuantity.innerHTML = product.quantity
                    productUnitPrice = document.createElement('td')
                    productUnitPrice.innerHTML = product.unit_price
                    var sellProduct = document.createElement('td')
                    sellProduct.innerHTML = '<button id="show">Sell</button>'

                    newRow.appendChild(productId)
                    newRow.appendChild(productCategory)
                    newRow.appendChild(productName)
                    newRow.appendChild(productQuantity)
                    newRow.appendChild(productUnitPrice)
                    newRow.appendChild(sellProduct)

                    tableBody.appendChild(newRow)
                }

            } else {
                invalid.textContent = '' + data.message
            }
        })
        .catch((err) => {
            console.log(err)
            invalid.textContent = "It's not you. It's us! Something went terribly wrong!"
        })
}

function sell(event) {
    event.preventDefault()
    let url = 'http://localhost:5000/api/v1/sales'
    let invalid = document.getElementById('invalid')
    let sellBtn = document.getElementById('show')
    let sale = sellBtn.parentElement.parentElement

    let productName = sale.children[2].textContent
    let quantity = document.getElementById('quantity')

    fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                name: productName,
                quantity: quantity.value
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === 'Sold!') {
                invalid.textContent = data.message
            } else {
                invalid.textContent = data.message
            }
        })
        .catch((err) => {
            console.log(err)
            invalid.textContent = "It's not you. It's us! Something went terribly wrong!"
        })
}