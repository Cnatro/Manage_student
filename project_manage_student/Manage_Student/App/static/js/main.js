$(document).ready(function(){
    document.getElementById('class_').addEventListener('change', function() {
        const selectedValue = this.value;
//        console.log(selectedValue)
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
               let $items= $('.show-student');
               $items[0].innerHTML = "";
               console.log($items)
               let index = 1;
               for( let key in data.students){
                    const student = data.students[key];
                    $items.append(`<tr>
                            <th scope="row">${index++}</th>
                            <td>${student.student_name}</td>
                            <td>${student.gender}</td>
                            <td>${student.birthday}</td>
                            <td>${student.address}</td>
                            <td>&times;</td>
                        </tr>`);
               };
          });
    });
});