function addToCart(id, MaLapTop, TenLapTop, DonGiaBan, Anh) {
    event.preventDefault();

    fetch('/api/add-cart', {
        method: 'POST',
        body: JSON.stringify({
            'id': id,
            'MaLapTop': MaLapTop,
            'TenLapTop': TenLapTop,
            'DonGiaBan': DonGiaBan,
            'Anh': Anh  // Make sure Anh is correctly passed as a string
        }),
        headers: {
            'Content-type': 'application/json'
        }
    }).then(function(res){
        return res.json();  // Convert response to JSON
    }).then(function(data){
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity;  // Update cart count
    }).catch(function(err){
        console.error(err);
    });
}


function Thanhtoan() {
    if (confirm('ban co muon thanh toan khong hoi that day? ')==true){
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data =>{   //cu phap t=round function giong lambda trong java
           if (data.code == 200 )
                location.reload()
        }).catch(err => console.error(err))
    }
}

function update_cart(id, obj){
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)

        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {  //data la ket qua chay tu res.json
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity;  // Update cart count

        let amount = document.getElementById('total-amount')
        amount.innerText= new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id) {
    if (confirm("ban chac chan xoa san pham nay khong? ")== true){
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {  //data la ket qua chay tu res.json
            let counter = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity;  // Update cart count

            let amount = document.getElementById('total-amount')
            amount.innerText= new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("laptop" + id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }

}