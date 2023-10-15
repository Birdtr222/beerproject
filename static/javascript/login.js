var setCookie = function(name, value, exp) {
	var date = new Date();
	date.setTime(date.getTime() + exp*24*60*60*1000);
	document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
};

var getCookie = function(name) {
	var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');

	return value? value[2] : null;
};

var deleteCookie = function(name) {
	document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
}
function Login() {
	let id = $('#id').val();
	let password = $( '#Pwd' ).val();
        $.ajax({
        type: "POST",
        url: "/login",
        data: {
            id: id,
            password: password
        },
        success: function (response) {
            if(response['msg']== "SUCCESS") {
                alert("로그인에 성공하였습니다.")
                window.location.reload()
                setCookie("access_token", response["access_token"])
                window.location.href="/"

            }
            else if (response['msg'] == "INVALID_ID") {
                alert("아이디가 틀렸습니다.")
            }
            else if(response['msg'] == "INVALID_PASSWORD") {
                alert("비밀번호가 틀렸습니다.")
            }
        }
    })
 }



