$(() => {
    // 返回按钮
    $('.box-footer button.back').click(() => {
        $('#content').load(
            $('.sidebar-menu li.active a').data('url'),
            (response, status, xhr) => {
                if (status !== 'success') {
                    message.showError('服务器超时，请重试！')
                }
            }
        );
    });
    // 保存按钮
    $('.box-footer button.save').click(function () {
        // 将表单中的数据进行格式化
        $
            .ajax({
                url: $(this).data('url'),
                data: $('form').serialize(),
                type: $(this).data('type')
            })
            .done((res) => {
                if (res['error'] === '0') {
                    message.showSuccess('修改分组成功！');
                    $('#content').load(
                        $('.sidebar-menu li.active a').data('url'),
                        (response, status, xhr) => {
                            if (status !== 'success') {
                                message.showError('服务器超时，请重试！')
                            }
                        }
                    );
                } else {
                    $('#content').html(res)
                }
            })
            .fail((res) => {
                message.showError('服务器超时，请重试！')
            })
    });

    // 复选框逻辑
    // 点击一级菜单，二级菜单联动
    // 注意要在一级菜单中class属性中加上one，二级菜单中加上two
    $('div.checkbox.one').each(function () {
        let $this = $(this);
        $this.find(':checkbox').click(function () {

            if($(this).is(':checked')){
                $this.siblings('div.checkbox.two').find(':checkbox').prop('checked', true)
            }else{
                $this.siblings('div.checkbox.two').find(':checkbox').prop('checked', false)

            }
        })
    });

    // 点击二级菜单，一级菜单联动
    $('div.checkbox.two').each(function () {
        let $this = $(this);
        $this.find(':checkbox').click(function () {
            if($(this).is(':checked')){
                $this.siblings('div.checkbox.one').find(':checkbox').prop('checked', true)
            }else {
                if(!$this.siblings('div.checkbox.two').find(':checkbox').is(':checked')){
                    $this.siblings('div.checkbox.one').find(':checkbox').prop('checked', false)
                }
            }
        })
    });
});