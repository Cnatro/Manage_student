document.addEventListener('DOMContentLoaded',function(){
    const form_change_class = document.getElementById('form-change-class');

    form_change_class.addEventListener('submit',function(event){
         is_error = false;
         const class_value = document.getElementById('class_none');
//         const check_class = document.querySelectorAll("input[name^='student_id']")
         if(class_value.value == ''){
            alert('Dữ liệu chưa được chọn!!');
            is_error = true;
         }
        if(is_error)
            event.preventDefault();
    });


    const form_adjust_grade = document.getElementById('form-adjust-grade');
    form_adjust_grade.addEventListener('submit',function(event){
         is_error = false;
         const grade_= document.getElementById('grade_');

         if(grade_.value == ''){
            alert('Dữ liệu chưa được chọn!!');
            is_error = true;
         }
        if(is_error)
            event.preventDefault();
    });
 });


function check_all_adjust(type=null){
    const parent_check = document.getElementById('parent-check');
    const child_checks = document.getElementsByClassName('child-check');

    if(type === 'parent')
        for (c of child_checks ){
            c.checked = parent_check.checked;
        }
    else if(type === null){
        let is_check = true;
        for (c of child_checks){
            if(!c.checked){
                is_check = false;
                break;
            }
        }
        parent_check.checked = is_check;
    }
}
