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