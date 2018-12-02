window.onload = () => {
    
    const url = 'http://localhost:5000/api/v1/sales'
    var token = localStorage.getItem('token')

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
            if (data.message === 'Sales fetched successfully!'){
                console.log(data.sales)
                for (let sale of data.sales){
                    newRow = document.createElement('tr')

                    attendant = document.createElement('td')
                    attendant.innerText = sale.sale_author
                    item = document.createElement('td')
                    item.innerText = sale.name
                    quantity = document.createElement('td')
                    quantity.innerText = sale.quantity
                    unitPrice = document.createElement('td')
                    unitPrice.innerText = sale.unit_price
                    totalPrice = document.createElement('td')
                    totalPrice.innerText = sale.total
                    date = document.createElement('td')
                    date.innerText = sale.purchase_date

                    newRow.appendChild(attendant)
                    newRow.appendChild(item)
                    newRow.appendChild(quantity)
                    newRow.appendChild(unitPrice)
                    newRow.appendChild(totalPrice)
                    newRow.appendChild(date)

                    tableBody.appendChild(newRow)
                }
            }else {
                invalid.textContent = data.message
            }
        })
        .catch((err) => {
            console.log(err)
            invalid.textContent = "It's not you. It's us! Something went terribly wrong!"
        })
}