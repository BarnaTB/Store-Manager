document.getElementById('submit-btn').addEventListener('click', addProduct)
document.getElementById('refresh').addEventListener('click', refreshTable)

const url = 'http://localhost:5000/api/v1/products'
var token = localStorage.getItem('token')


function addProduct(event){
    event.preventDefault()
    let category = document.getElementById('category')
    let name = document.getElementById('name')
    let quantity = document.getElementById('quantity')
    let unitPrice = document.getElementById('unit-price')
    
    let productId = document.getElementById('product-id')
    let productCategory = document.getElementById('product-category')
    let productName = document.getElementById('product-name')
    let productQuantity = document.getElementById('product-quantity')
    let productUnitPrice = document.getElementById('product-unitprice')
    let deleteProduct = document.getElementById('delete-product')

    let invalid = document.getElementById('invalid')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
        body: JSON.stringify({category: category.value, name: name.value, quantity: quantity.value, unit_price: unitPrice.value})
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.message === 'Product added successfully!'){                
                productId.textContent = "" + data.product._id
                productCategory.innerHTML = "" + data.product.category + '<button type="submit">Modify</button>'
                productName.innerHTML = "" + data.product.name + '<button type="submit">Modify</button>'
                productQuantity.innerHTML = "" + data.product.quantity + '<button type="submit">Modify</button>'
                productUnitPrice.innerHTML = "" + data.product.unit_price + '<button type="submit">Modify</button>'
                deleteProduct.innerHTML = '<button type="submit" id="delete-btn">Delete</button>'
                invalid.textContent = data.message 
            }else{
                invalid.textContent = data.message
            }
        })
        .catch((err) => console.log(err), invalid.textContent = "It's not you. It's us! Something went terribly wrong!")

}

function refreshTable(){
    event.preventDefault()
    let invalid = document.getElementById('invalid')
    let tableBody = document.querySelector('#table > tbody')

    fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.message === 'Products Fetched!'){
                for (let product of data.products){
                    newRow = document.createElement('tr')
                    productId = document.createElement('td')
                    productId.textContent = product._id
                    productCategory = document.createElement('td')
                    productCategory.innerHTML = '' + product.category + '<button type="submit">Modify</button>'
                    productName = document.createElement('td')
                    productName.innerHTML = '' + product.name + '<button type="submit">Modify</button>'
                    productQuantity = document.createElement('td')
                    productQuantity.innerHTML = '' + product.quantity + '<button type="submit">Modify</button>'
                    productUnitPrice = document.createElement('td')
                    productUnitPrice.innerHTML = '' + product.unit_price + '<button type="submit">Modify</button>'
                    deleteProduct = document.createElement('td')
                    deleteProduct.innerHTML = '<button type="submit" id="delete-btn">Delete</button>'

                    newRow.appendChild(productId)
                    newRow.appendChild(productCategory)
                    newRow.appendChild(productName)
                    newRow.appendChild(productQuantity)
                    newRow.appendChild(productUnitPrice)
                    newRow.appendChild(deleteProduct)

                    tableBody.appendChild(newRow)
                }
                
            }else{
                invalid.textContent = '' + data.message
            }
        })
        .catch((err) => console.log(err))
}