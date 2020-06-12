$(() => {
    let $sideBar = $('.sidebar-menu');                                  // 边栏ul
    let $bars = $('.sidebar-menu').find('li:not(.treeview)');       // 所有的菜单

    $bars.click(function () {
        $this = $(this);
        // 改变样式
        $bars.removeClass('active');
        $this.addClass('active');
        // 点击没有子菜单的一级菜单，要关闭其他打开了的一级菜单
        // jq的对象不能比较，转换成dom对象
        if ($this.parent()[0] === $sideBar[0]) {
            // 关闭打开的二级菜单
            $sideBar.children('li.treeview.menu-open').children('ul').slideUp();
            $sideBar.children('li.treeview.menu-open').removeClass('menu-open')
        }

        // 发送ajax，动态的修改content
        $('#content').load($this.children('a:first').data('url'), (res, status, xhr) => {
            if (status !== 'success') {
                message.showError('服务器超时，请重试！')
            }
        })
    });

    // 首次访问 触发第一个菜单的加载
    $bars[0].click();

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
});