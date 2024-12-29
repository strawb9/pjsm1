add_column = 0
quantity_student = 0
quantity_row = 0


function Timkiemlop(){
    fetch("/api/Timkiemlop", {
        method: "post",
        body: JSON.stringify({
            "timkiemlop" : document.getElementById('timkiemlop').value,
            "num_row_15m" : document.getElementById('num_row_15m').value,
            "num_row_45m" : document.getElementById('num_row_45m').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let table_score = document.getElementsByClassName('table_score')
        for (let t of table_score)
            t.style.display = "inline"
        let tenLop = document.getElementById('tenLop')
        tenLop.innerHTML = `Lớp: ${data[0].tenLop}`
        document.getElementById('bt1').blur()
        quantity_student = data[0].quantity

        a=document.getElementsByClassName('add_col')
        while(a.length!=0){
            a[0].remove()
        }

        themcot(data[0].num_row_15m, 'Điểm 15 phút')
        themcot(data[0].num_row_45m, 'Điểm 45 phút')
        themcot(1, 'Điểm cuối kỳ')

        b=document.getElementsByClassName('add_row')
        while(b.length!=0){
            b[0].remove()
        }

        for(let i = 1; i <= data[0].quantity; i++)
        {
            let input_score = document.getElementById('input_score')
            var row = document.createElement('tr')
            row.classList.add('add_row')
            var id = document.createElement('td')
            var textNode = document.createTextNode(data[i].id)
            id.appendChild(textNode)
            row.appendChild(id)
            var name = document.createElement('td')
            textNode = document.createTextNode(data[i].name)
            name.appendChild(textNode)
            row.appendChild(name)
            add_column = parseInt(data[0].num_row_15m)+parseInt(data[0].num_row_45m)+parseInt(1)
            for (let j =0; j< add_column; j++)
            {
                var input = document.createElement('td')
                textNode = document.createElement('input')
                textNode.classList.add('mt-3')
                textNode.classList.add('mb-3')
                textNode.classList.add('ms-3')
                textNode.classList.add('me-3')
                textNode.classList.add('input_score')
                textNode.type = 'number'
                textNode.placeholder = ''
                textNode.id = `${i-1}_${j}`
                input.appendChild(textNode)
                row.appendChild(input)
            }
            input_score.appendChild(row)
        }
    });
}

function themcot(quantity, name){
    table_col = document.getElementById('table_col')
    for(let i = 0; i < quantity; i++)
    {
        var add_col = document.createElement('th')
        add_col.classList.add('add_col')
        var textNode = document.createTextNode(name)
        add_col.appendChild(textNode)
        table_col.appendChild(add_col)
    }
}

function Luudiem(){
    fetch("/api/Luudiem", {
        method: "post",
        body: JSON.stringify({
            "scores": getDiem(),
            "monHoc_id": document.getElementById('monHoc_id').value,
            "hocki_id": document.getElementById('hocki_id').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        alert(data.content)
    });
}

function getDiem(){
    var arr = []
    for(var i = 0; i < quantity_student; i++)
    {
        var row = []
        for(var j = 0; j < add_column; j++)
        {
            var col = document.getElementById(`${i}_${j}`).value
            row.push(col)
        }
        arr.push(row)
    }
    return arr
}

function Xuatdiemm(){
    fetch("/api/Xuatdiemm", {
        method: "post",
        body: JSON.stringify({
            "lop_id": document.getElementById('lop_id').value,
            "hocki_id": document.getElementById('hocki_id').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        result = document.getElementById('result')
        result.style.display = 'inline'
        schoolyear = document.getElementById('schoolyear')
        schoolyear.innerHTML = `${data[0].schoolyear}`
        table_result = document.getElementById('table_result')
        for(var i = 0; i < quantity_row; i++)
            table_result.deleteRow(1)

        quantity_row = data[0].quantity
        for(var i = 1; i <= data[0].quantity; i++)
        {
            var row = table_result.insertRow()
            row.insertCell().innerText = i
            row.insertCell().innerText = data[i].tenHs
            row.insertCell().innerText = data[0].class
            row.insertCell().innerText = data[i].semester_1
            row.insertCell().innerText = data[i].semester_2
        }
    });
}