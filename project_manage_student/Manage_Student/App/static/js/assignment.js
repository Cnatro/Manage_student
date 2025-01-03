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

function get_subject_semester_year_by_class(){
    const selectedValue = document.getElementsByClassName('class_in_teacher_score').value;
    const object_list = document.getElementsByClassName('object_in_teacher_score');
    const semster_list = document.getElementsByClassName('semester_in_teacher_score');
    const year_list = document.getElementsByClassName('year_in_teacher_score');

    object_list.innerHTML = ""
    semster_list.innerHTML = ""
    year_list.innerHTML = ""
//    console.info(selectedValue);
    fetch('/api/teacher_score',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            'class_in_teacher_score':selectedValue
        })
    }).then(res => res.json())
      .then(data => {
//            console.info(data.class_list)
            data.object_list.forEach((o) =>{
                var option_ = document.createElement('option');
                option_.value = `${o.object_id}`;
                option_.textContent = `${o.object_name}`;
                object_list.append(option_);

                // kích hoạt sự kiện onchange luôn khi mới tạo
                object_list.dispatchEvent(new Event('change'));
            })
            data.semester_list.forEach((i) =>{
                var option_ = document.createElement('option');
                option_.value = `${i.object_id}`;
                option_.textContent = `${i.object_name}`;
                object_list.append(option_);

                // kích hoạt sự kiện onchange luôn khi mới tạo
                semester_list.dispatchEvent(new Event('change'));
            })
            data.year_list.forEach((c) =>{
                var option_ = document.createElement('option');
                option_.value = `${c.object_id}`;
                option_.textContent = `${c.object_name}`;
                object_list.append(option_);

                // kích hoạt sự kiện onchange luôn khi mới tạo
                year_list.dispatchEvent(new Event('change'));
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