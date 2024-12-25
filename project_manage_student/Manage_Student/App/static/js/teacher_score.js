document.addEventListener('DOMContentLoaded',function(){
    const input_score = document.querySelectorAll('input[type="number"]');
    for( ip of input_score ){
        if(ip.value != '')
            ip.disabled = true;
    }
});

function get_info_by_class(){

    const class_ = document.getElementById('class-select');
    fetch('/api/teacher_score/get_info_by_class',{
        method:'post',
        body:JSON.stringify({
            'class_id':class_.value
        }),
        headers:{
           'Content-Type' : 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        console.log(data)
        const subject_id = document.getElementById('subject-id');
        const semester_name = document.getElementById('semester-name');
        const semester_year = document.getElementById('semester-year');

        subject_id.innerHTML = '';
        semester_year.innerHTML = '';

        semester_year.value = `${data.year}-2025`;

        data.subjects.forEach(dt => {
            const option  = document.createElement('option');
            option.value = `${dt.subject_id}`;
            option.textContent = `${dt.subject_name}`;
            subject_id.append(option);
        })
        subject_id.addEventListener('change',function(){
                semester_name.innerHTML = '';
                data.values[this.value].forEach( val =>{
                const option = document.createElement('option');
                option.value = `${val.semester_id}`;
                option.textContent = `${val.semester_name}`;

                semester_name.append(option);
            } )
        });
        subject_id.dispatchEvent(new Event('change'));
    });
}

function saveScore(teacher_plan_id){
    const score=[];
    const input_score = document.querySelectorAll('input[type="number"]');

    for( ip of input_score ){
        score.push({
            'student_id':ip.dataset.id,
            'type_exam':ip.className.slice(0,-2),
            'value':ip.value,
            'count_exam':ip.className.slice(-1)
        });
    }

    fetch(`/api/teacher_score/${teacher_plan_id}/score`,{
        method:'post',
        body:JSON.stringify({
            'list_score':score
        }),
        headers:{
           'Content-Type' : 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        if (data.status === 200) {
             confirm("Lưu thành công!");
             window.location.href = `/teacher/view_score/${teacher_plan_id}`;
        }
    });
}

function editScore(student_id,teacher_plan_id){
    const input_score = document.querySelectorAll(`input[data-id="${student_id}"]`);
    for( ip of input_score ){
        ip.disabled = ! ip.disabled;
    }

    const div_action = document.querySelector(`div.action[data-id="${student_id}"]`);
    div_action.innerHTML = `
                <button class="btn btn-primary" onclick="confirm_edit(${student_id},${teacher_plan_id})">Xác nhận</button>
                <button class="btn btn-danger" onclick="cancel_edit(${student_id},${teacher_plan_id})">Hủy</button>
    `;
}

function confirm_edit(student_id,teacher_plan_id){
    const input_score = document.querySelectorAll(`input[data-id="${student_id}"]`);
    score=[];
    for( ip of input_score ){
        if(ip.value != ''){
            score.push({
                'student_id':ip.dataset.id,
                'type_exam':ip.className.slice(0,-2),
                'value':ip.value,
                'count_exam':ip.className.slice(-1)
             });
        }
    }
    fetch(`/api/teacher_score/${teacher_plan_id}/edit_score`,{
        method:'put',
        body:JSON.stringify({
            'list_score':score
        }),
        headers:{
           'Content-Type' : 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        console.log(data)
        if (data.status === 200) {
             confirm("Đã sửa điểm thành công!");
             window.location.href = `/teacher/teacher_input_score/${teacher_plan_id}`;
        }
    });
}

function cancel_edit(student_id,teacher_plan_id){
     const input_score = document.querySelectorAll(`input[data-id="${student_id}"]`);
        for( ip of input_score ){
            ip.disabled = ! ip.disabled;
        }

    const div_action = document.querySelector(`div.action[data-id="${student_id}"]`);
    div_action.innerHTML = `
               <button class="btn btn-danger" onclick="editScore(${student_id},${teacher_plan_id})">Sửa</button>
    `;
    window.location.reload();
}