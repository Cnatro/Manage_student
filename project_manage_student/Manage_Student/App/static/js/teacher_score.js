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
        console.log(data);
    });
}
