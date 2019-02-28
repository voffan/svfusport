
var obj;

function myFunk(x){
    var t = document.getElementById(x);
    if (obj != t){
        if (obj) obj.style.display = 'none';

        t.style.display = 'block';
        obj = t;
    }

    else {
        t.style.display = 'none';
        obj = null;
    }
}




