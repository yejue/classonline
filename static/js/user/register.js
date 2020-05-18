$(
    () => {
        // 点击刷新验证码
        $('.captcha-graph-img img').click(function () {
                $(this).attr('src', '/veri/image_code?rand=' + Math.random());
            }
        )
    }
);


// 定义一些状态变量

let isUsernameReady = false,    // 用户名状态
    isPasswordReady = false,     // 密码状态
    isMobileReady = false,       // 手机号
    isSmsCodeReady = false;       // 短信验证码


// 用户名校验 onblur
let $username = $('#user_name');
$username.blur(checkUsername);

function checkUsername() {
    isUsernameReady = false;
    // 取得用户名
    $sUsername = $username.val();

    if (!$sUsername) {
        message.showError('用户名不能为空');
        return
    } else if (!(/^\w{5,20}$/).test($sUsername)) {
        message.showError('请输入5~20位的字母或数字用户名');
        return
    }

    // 发送ajax
    $.ajax({
        url: '/veri/check=' + $sUsername + '/',
        type: 'GET',
        dataType: 'JSON',
        success: function (res) {
            if (res['data']['count'] !== 0) {
                message.showError('用户名已被注册')
            } else {
                isUsernameReady = true;
                message.showInfo('该用户名可以正常使用')
            }
        },
        error: function () {
            message.showError('服务器超时，请重试')
        }
    })
}


// 密码
let $password = $('#pwd'),
    $passwordRepeat = $('input[name="password_repeat"]');

$password.blur(password_format);
$passwordRepeat.blur(password_equal);

// 密码格式校验
function password_format(){
    if (!(/^.{5,20}$/).test($password.val())){
        message.showError('密码格式必须为5~20位字符串')
    }
}
// 两次密码是否一致
function password_equal(){
    isPasswordReady = false;
    if (!$passwordRepeat.val()){
        message.showError('密码不能为空')
        return
    }
    if (!(/^.{5,20}$/).test($password.val())){
        message.showError('密码格式必须为5~20位字符串')
        return
    }
    if ($password.val() !== $passwordRepeat.val()){
        message.showError('两次输入的密码不正确，请重新输入')
    }else{
        isPasswordReady = true
    }

}
// 手机号校验是否存在

let $mobile = $('#mobile');
$mobile.blur(checkMobile);

function checkMobile() {
    isMobileReady = false;
    // 取得手机号
    $sMobile = $mobile.val();

    if (!$sMobile) {
        message.showError('手机号不能为空');
        return
    } else if (!(/^1[3456789]\d{9}$/).test($sMobile)) {
        message.showError('请输入正确的手机号');
        return
    }

    // 发送ajax
    $.ajax({
        url: '/veri/mobile=' + $sMobile + '/',
        type: 'GET',
        dataType: 'JSON',
    })
        .done(function (res) {
            if (res['data']['count'] !== 0) {
                message.showError('手机号已被注册')
            } else {
                isMobileReady = true;
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}


// 发送短信验证码
let $sms_captcha = $('.sms-captcha');
$sms_captcha.click(smsButton);

function smsButton() {
    // 取得手机号
    // 取得图形验证码
    let $sImageCaptcha = $('#input_captcha').val();
    if (!$sImageCaptcha) {
        message.showError('图形验证码不能为空');
        return
    }

    if (!isMobileReady) {
        checkMobile();
        return
    }


    // 发送ajax
    $.ajax({
        url: '/veri/sms_code/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            mobile: $sMobile,
            captcha: $sImageCaptcha
        }
    })
        .done(function (res) {
            if (res['error'] != 0) {
                message.showError(res['errmsg'])
            } else {
                $sms_captcha.attr('disabled', true);
                var num = 60;
                let t = setInterval(function () {
                    $sms_captcha[0].innerText = num;
                    if (num === 1) {
                        clearInterval(t);
                        $sms_captcha[0].innerText = '获取验证码';
                        $sms_captcha.removeAttr('disabled');
                    }
                    num--;
                }, 1000)
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}

// 注册功能
let $registerBtn = $('.register-btn');
$registerBtn.click(registerFn);

let $sms_input = $('#input_smscode')
$sms_input.blur(smsInput)

function smsInput() {
    isSmsCodeReady = false;

    if ($sms_input.val()){
        isSmsCodeReady = true
    }else{
        message.showError('请输入短信验证码');
    }
}

function registerFn(e) {
    e.preventDefault();

    if (!isUsernameReady) {
        checkUsername();
        return
    } else if (!isPasswordReady) {
        password_equal();
        return;
    } else if (!isMobileReady) {
        checkMobile();
        return
    } else if (!isSmsCodeReady) {
        smsInput()
        return
    }

    $.ajax({
        url: '/user/register/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            username: $sUsername,
            password: $password.val(),
            password_repeat: $passwordRepeat.val(),
            sms_code: $('#input_smscode').val(),
            mobile: $sMobile

        }
    })
        .done(function (res) {
            if (res['error'] != 0) {
                message.showError(res['errmsg'])
            } else {
                message.showSuccess('注册成功，即将跳转至登录页面')
                // 跳转到登录页面
                setTimeout(()=>{
                    window.location.href = '/user/login'
                }, 1500)
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}