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
            console.info(data.class_list)
            data.class_list.forEach((c) =>{
                var option_ = document.createElement('option');
                option_.value = `${c.class_id}`;
                option_.textContent = `${c.class_name}`;
                class_list.append(option_);
            })
      });
}
