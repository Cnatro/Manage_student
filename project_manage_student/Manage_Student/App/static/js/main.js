function get_students_by_class(columns,type=false){
    const selectedValue = document.getElementById("class_").value;
        fetch('/api/student_class',{
              method:'post',
              headers:{
                'Content-Type' : 'application/json'
              },
              body:JSON.stringify({
                   'class_id':selectedValue
              })
        }).then(res => res.json())
          .then(data => {
               // cập nhật học sinh
               let $items= $('.show-student');
               $items[0].innerHTML = "";
               let index = 1;
               for( let key in data.students){
                    const student = data.students[key];
                    let row = `<tr>
                        <th scope="row">${index++}</th>`;

                        // Lặp qua các cột được chỉ định
                        columns.forEach(col => {
                            row += `<td>${student[col] || 'chưa cập nhật'}</td>`;
                        });
                        if(type === true){
                            row += `<td><input class="form-check-input mt-2 mb-2 child-check" type="checkbox"
                             name='student_id' value='${student.student_id}' onchange="check_all_adjust()"/></td>`
                        }else
                            row += `<td>&times;</td>`; // Cột "action" mặc định
                        row += `</tr>`;
                        $items.append(row);
               };
               // cập nhật sỉ số
//                let quantity_student = getElementById('quantity_student');
//                quantity_student.innerText = data.total_quantity;
          });
}