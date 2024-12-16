//nút tìm chỗ search
document.addEventListener('DOMContentLoaded',function(){
    let form = document.getElementById('search-assignment');
    let grade = document.getElementById('grade');
    let class_ = document.getElementById('class_');

    if(form){
            form.addEventListener('submit', function (event) {
            if (grade.value === '' || class_.value === '') {
                event.preventDefault(); // Ngăn chặn gửi form
                alert('Vui lòng chọn đầy đủ thông tin Khối và Lớp trước khi tìm kiếm!');
            }
        });
    }

//    btn save
    let form_assignment = document.getElementById('form-assignment');
    if( form_assignment ){
        form_assignment.addEventListener('submit',function(event){
            const teacherSelects = document.querySelectorAll("select[name^='teacher_subject_id']");
            is_error = false;

            for( t of teacherSelects ){
                if(t.value === ''){
                    alert('Vui lòng chọn đầy đủ giáo viên phân công!!');
                    is_error = true;
                    break;
                }
            }
            if(is_error)
                event.preventDefault();

        });
    }

});
//==========================
function get_class_by_grade(){
    const selectedValue = document.getElementById('grade').value;
    const class_list = document.getElementById('class_');
    class_list.innerHTML = ""
//    console.info(selectedValue);
    fetch('/api/teacher_assignment',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            'grade':selectedValue
        })
    }).then(res => res.json())
      .then(data => {
//            console.info(data.class_list)
            data.class_list.forEach((c) =>{
                var option_ = document.createElement('option');
                option_.value = `${c.class_id}`;
                option_.textContent = `${c.class_name}`;

                class_list.append(option_);
                // kích hoạt sự kiện onchange luôn khi mới tạo
                class_list.dispatchEvent(new Event('change'));
            })
      });
}

function check_semester(subject_id,type_semester){
    const semesters = document.getElementById(`semesters-${subject_id}`);
    const semester1 = document.getElementById(`semester1-${subject_id}`);
    const semester2 = document.getElementById(`semester2-${subject_id}`);

    if(type_semester == 'total'){
        if(semesters.checked === true){
            semester1.checked = true;
            semester2.checked = true;
        }else
        {
            semester1.checked = false;
            semester2.checked = false;
        }
    }else{
        if(semester1.checked == false || semester2.checked == false){
            semesters.checked = false;
        }
        if(semester1.checked == true && semester2.checked == true)
            semesters.checked = true;
    }

}

function value_of_semesters(){
    const semester_year = document.getElementById('learn_year').value;
    fetch('/api/teacher_assignment/get_value_year',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            'year':semester_year
        })
    }).then(res => res.json())
      .then(data => {
            const semester1s = document.getElementsByClassName('semester1');
            const semester2s = document.getElementsByClassName('semester2');

            for( s of semester1s ){
               let name = data.values.find( item => item.name === 'HK1')
               if(name) s.value = name.id;
            }

            for( s of semester2s ){
               let name = data.values.find( item => item.name === 'HK2')
               if(name) s.value = name.id;
            }
      });
}