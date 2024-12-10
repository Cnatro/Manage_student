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