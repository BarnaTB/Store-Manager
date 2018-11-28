document.getElementById('add-btn').addEventListener('click', addProduct)
document.getElementById('refresh').addEventListener('click', refreshTable)
document.getElementById('show').addEventListener('click', modifyPopUp)
document.getElementById('modify-btn').addEventListener('click', modifyProduct)

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
    const deletePdt = document.getElementById('delete-product')

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
                productCategory.innerHTML = "" + data.product.category
                productName.innerHTML = "" + data.product.name
                productQuantity.innerHTML = "" + data.product.quantity
                productUnitPrice.innerHTML = "" + data.product.unit_price
                deletePdt.innerHTML = '<button type="submit" id="delete-btn">Delete</button>'
                deletePdt.addEventListener('click', deleteProduct(deletePdt))
                invalid.textContent = data.message 
            }else{
                invalid.textContent = data.message
            }
        })
        .catch((err) => console.log(err), invalid.textContent = "It's not you. It's us! Something went terribly wrong!")

}

function refreshTable(){
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
                    productCategory.innerHTML = '' + product.category
                    productName = document.createElement('td')
                    productName.innerHTML = '' + product.name
                    productQuantity = document.createElement('td')
                    productQuantity.innerHTML = '' + product.quantity
                    productUnitPrice = document.createElement('td')
                    productUnitPrice.innerHTML = '' + product.unit_price
                    deletePdt = document.createElement('td')
                    deletePdt.innerHTML = '<button type="submit" id="delete-btn">Delete</button>'
                    deletePdt.addEventListener('click', deleteProduct)

                    newRow.appendChild(productId)
                    newRow.appendChild(productCategory)
                    newRow.appendChild(productName)
                    newRow.appendChild(productQuantity)
                    newRow.appendChild(productUnitPrice)
                    newRow.appendChild(deletePdt)

                    tableBody.appendChild(newRow)
                }
                
            }else{
                invalid.textContent = '' + data.message
            }
        })
        .catch((err) => {
            console.log(err)
            invalid.textContent = "It's not you. It's us! Something went terribly wrong!"
        })
}

function modifyPopUp(event){
    event.preventDefault()
    $('#show').on('click', () => {
        $('.center').show()
        $('#show').hide()
    })

    $('#close').on('click', () => {
        $('#show').show()
        $('.center').hide()
    })
}

function modifyProduct(event){
    event.preventDefault()
    let productID = document.getElementById('modify-id')
    let newCategory = document.getElementById('modify-category')
    let newName = document.getElementById('modify-name')
    let newQuantity = document.getElementById('modify-quantity')
    let newUnitPrice = document.getElementById('modify-unitprice')
    let invalid = document.getElementById('invalid')

    fetch(url + '/' + productID.value, {
        method: 'PUT',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
        body: JSON.stringify({category: newCategory.value, name: newName.value, quantity: newQuantity.value, unit_price: newUnitPrice.value})
    })
    .then((response) => response.json())
        .then((data => {
            if (data.message === 'Product updated!'){
                invalid.textContent = data.message + ' ' + 'Please refresh table to see changes!'
                location.reload()
            }else{
                invalid.textContent = data.message
            }
        }))
        .catch((err) => console.log(err), invalid.textContent = "It's not you. It's us! Something went terribly wrong!")
}


function deleteProduct(event){
    event.preventDefault()
    let deleteBtn = document.getElementById('delete-btn')
    let invalid = document.getElementById('invalid')
    const parent = deleteBtn.parentElement.parentElement
    let product = parent.children

    let productId = product.item(0).textContent

    fetch(url + '/' + productId, {
        method: 'DELETE',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.message === 'Product deleted!'){
                invalid.textContent = data.message + 'Refresh page and table to view your new inventory!'
            }else{
                invalid.textContent = data.message
            }
        })
        .catch((err) => console.log(err), invalid.textContent = "It's not you. It's us! Something went terribly wrong!")
}