// 넘어 온 값이 빈값인지 체크
// [],{}도 빈값으로 처리
let isEmpty = function(value){
    if("" == value || null == value || undefined == value
    || (value != null && typeof value == "object" && !Object.keys(value).length) ){
        return true;
    }
    else{
        return false;
    }
};