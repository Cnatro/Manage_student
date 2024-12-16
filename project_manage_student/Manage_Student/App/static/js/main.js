// thông báo thành công or thất bại
 document.addEventListener('DOMContentLoaded',function(){
 // ủy quyền sự kiện khi người dùng nhấn vào .delete thì sự kiện ms đc kích hoạt
        $('.show-student').on('click','.delete-student',function(event){
            event.preventDefault()

            let result = confirm('Bạn chắc chắn muốn xóa');
            if( result ){
                window.location.href = this.href;
                confirm('Bạn đã xóa thành công');
            }
        })
 });
//=====================================

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

                        columns.forEach(col => {
                            row += `<td>${student[col] || 'chưa cập nhật'}</td>`;
                        });

                        if(type === true){
                            row += `<td><input class="form-check-input mt-2 mb-2 child-check" type="checkbox"
                             name='student_id' value='${student.student_id}' onchange="check_all_adjust()"/></td>`
                        }else{
                             row += `<td><a class="text-danger delete-student" href="/staff/manage_student/delete/${student.student_id}"> <i class="fa-regular fa-trash-can"></i> </a></td>`;
                        }

                        row += `</tr>`;
                        $items.append(row);
               };
          });
}

function search_name_student(columns,type=false){
    let value_search = document.getElementById('search').value;
    const class_id = document.getElementById("class_").value;
    fetch('/api/student_class/search',{
        method:'post',
        headers:{
           'Content-Type' : 'application/json'
        },
        body:JSON.stringify({
            'value_search':value_search,
            'class_id':class_id
        })
    }).then( res => res.json())
      .then( data => {
            let $items= $('.show-student');
               $items[0].innerHTML = "";
               let index = 1;
               for( let key in data.students){
                    const student = data.students[key];
                    let row = `<tr>
                        <th scope="row">${index++}</th>`;
                        columns.forEach(col => {
                            row += `<td>${student[col] || 'chưa cập nhật'}</td>`;
                        });

                        if(type === true){
                            row += `<td><input class="form-check-input mt-2 mb-2 child-check" type="checkbox"
                             name='student_id' value='${student.student_id}' onchange="check_all_adjust()"/></td>`
                        }else{
                             row += `<td><a class="text-danger delete-student" href="/staff/manage_student/delete/${student.student_id}"><i class="fa-regular fa-trash-can"></i></a></td>`;
                        }

                        row += `</tr>`;
                        $items.append(row);
               };
      });
}