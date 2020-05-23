// 定义一些状态变量

let isAccountReady = false,    // 用户名状态
    isPasswordReady = false;    // 密码状态

// 用户名校验 onblur
let $account = $('input[name="account"]');

function checkAccount(msg='') {
    isAccountReady = false;
    // 取得用户名
    $sAccount = $account.val();

    if (!$sAccount) {
        if(msg){
            message.showError(msg)
        }
    } else if (!(/^\w{5,20}$/).test($sAccount)) {
        message.showError('请输入5~20位的字母或数字用户名');
    }}
// 密码
let $password = $('input[name="password"]');

// 密码校验
function checkLoginPassword(msg=''){
    isPasswordReady = false;
    if (!$password.val()){
        if(msg){
            message.showError(msg)
        }
    }else{
        isPasswordReady = true
    }
}


// 登录功能
let $loginBtn = $('.login-btn');
$loginBtn.click(loginFn);

function loginFn(e) {
    e.preventDefault();
    if (!isAccountReady) {
        checkAccount('用户名或密码不能为空');
        return
    } else if (!isPasswordReady) {
        checkLoginPassword('用户名或密码不能为空');
        return
    }

    $.ajax({
        url: '/user/login/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            account: $account.val(),
            password: $password.val(),
        }
    })
        .done(function (res) {
            if (res['error'] !== 0) {
                message.showError(res['errmsg'])
            } else {
                message.showSuccess('登录成功，正在跳转')
                // 跳转到登录页面
                setTimeout(()=>{
                    if (!document.referrer | document.referrer==='/user/login'
                        | document.referrer==='/user/register'){
                        window.location.href = '/'
                    }else{
                        window.location.href = document.referrer
                    }
                }, 1500)
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}