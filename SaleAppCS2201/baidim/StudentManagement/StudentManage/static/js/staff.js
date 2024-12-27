let quantity_student = 0
let quantity_student_in_class = 0
lop_id = 0

function changeClass() {
    fetch("/api/changeClass", {
        method: "post",
        body: JSON.stringify({
            "hs_id" : document.getElementById('hs_id').value,
            "lop_id" : document.getElementById('lop_id').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        document.getElementById('btn_changeClass').blur()
        let a = document.getElementById('changeClass')
        if(data.content === "Thành công")
            a.innerHTML = `<div class="alert alert-success">${data.content}</div>`
        else
            a.innerHTML = `<div class="alert alert-danger">${data.content}</div>`
    });
}

function searchStudent() {
    fetch("/api/searchStudent", {
        method: "post",
        body: JSON.stringify({
            "searchstudent" : document.getElementById('searchstudent').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        if (data[0].quantity === 0)
        {
            let a = document.getElementById('no_result_searchstudent')
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-success">Không tìm thấy học sinh</div>`
            let b = document.getElementById('result_searchstudent')
            b.style.display = "none"
        }
        else
        {
            let b = document.getElementById('no_result_searchstudent')
            b.style.display = "none"
            let a = document.getElementById('result_searchstudent')
            a.style.display = "inline"
            let table = document.getElementById('table_result')

            for (let j =1; j <= quantity_student; j++)
                table.deleteRow(1)

            quantity_student = data[0].quantity

            for (let j = 1; j <= data[0].quantity; j++)
            {
                var row = table.insertRow()
                row.insertCell().innerText = data[j].id
                row.insertCell().innerText = data[j].tenHs
                row.insertCell().innerText = data[j].lop
            }
        }

    });
}

function printClass(id) {
    fetch("/api/printClass", {
        method: "post",
        body: JSON.stringify({
            "lop_id" : id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let id = document.getElementById(data[0].id)
        id.classList.add("active")
        if (lop_id != 0)
        {
            let id_remove = document.getElementById(lop_id)
            id_remove.classList.remove("active")
        }

        lop_id = data[0].id
        let a = document.getElementById('no_student')
        let b = document.getElementById('print_class')
        if(data[0].quantity == 0)
        {
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-info text-center">Lớp không có học sinh</div>`
            b.style.display = "none"
        }
        else
        {
            let tenLop = document.getElementById('tenLop')
            tenLop.innerText = `Lớp: ${data[0].class}`
            let quantity = document.getElementById('quantity')
            quantity.innerText = `Sĩ số: ${data[0].quantity}`

            a.style.display = "none"
            b.style.display = "inline"
            let table = document.getElementById('table_print_class')

            for(let i = 1; i <= quantity_student_in_class; i++)
                table.deleteRow(1)

            quantity_student_in_class = data[0].quantity

            for(let i = 1; i <= data[0].quantity; i++)
            {
                var row = table.insertRow()
                row.insertCell().innerText = i
                row.insertCell().innerText = data[i].tenHs
                row.insertCell().innerText = data[i].gioiTinh
                row.insertCell().innerText = data[i].ngaysinh
                row.insertCell().innerText = data[i].diaChi
            }
        }
    });
}

function printClassPrevious(){
    if (lop_id == 0)
        printClass(15)
    else if (lop_id == 1)
        printClass(15)
    else
        printClass(lop_id - 1)
}

function printClassNext(){
    if (id_class == 0)
        printClass(1)
    else if (id_class == 15)
        printClass(1)
    else
        printClass(id_class + 1)
}