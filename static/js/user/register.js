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
    isImageCodeReady = false,    // 图形验证码
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
        url: '/user/check=' + $sUsername + '/',
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

// 密码校验是否相同

let $pwdRepeat = $('input[name="password_repeat"]');
$pwdRepeat.blur(passwd_repeat);

function passwd_repeat() {
    // 状态变更
    isPasswordReady = false;

    let $password = $('#pwd').val(),
        $sPwdRepeat = $pwdRepeat.val();

    if (!($password === $sPwdRepeat)) {
        message.showError('两次输入的密码不一致，请确认后输入')
    } else {
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
        url: '/user/mobile=' + $sMobile + '/',
        type: 'GET',
        dataType: 'JSON',
    })
        .done(function (res) {
            if (res['data']['count'] !== 0) {
                message.showError('手机号已被注册')
            } else {
                isUsernameReady = true;
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}


