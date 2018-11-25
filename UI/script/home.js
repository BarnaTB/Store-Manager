document.getElementById('refresh').addEventListener('click', refreshTable)

const url = 'http://localhost:5000/api/v1/products'
var token = localStorage.getItem('token')

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
                console.log(data.products)
                for (let product of data.products){
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
                    sellProduct = document.createElement('td')
                    sellProduct.innerHTML = '<button type="submit">Sell</button>'

                    newRow.appendChild(productId)
                    newRow.appendChild(productCategory)
                    newRow.appendChild(productName)
                    newRow.appendChild(productQuantity)
                    newRow.appendChild(productUnitPrice)
                    newRow.appendChild(sellProduct)

                    tableBody.appendChild(newRow)
                }
                
            }else{
                invalid.textContent = '' + data.message
            }
        })
        .catch((err) => console.log(err))
}