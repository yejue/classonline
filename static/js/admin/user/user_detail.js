$(() => {
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

    $('.box-footer button.save').click(function () {
        $
            .ajax({
                url: $(this).data('url'),
                data: $('form').serialize(),
                type: 'PUT'
            })
            .done((res) => {
                if (res['error'] === '0') {
                    message.showSuccess('修改用户成功！');
                    $('#content').load(
                        $('.sidebar-menu li.active a').data('url'),
                        (response, status, xhr) => {
                            if (status !== 'success') {
                                message.showError('服务器超时，请重试！')
                            }
                        }
                    );
                }else {
                    $('#content').html(res)
                }
            })
            .fail((res)=>{
                message.showError('服务器超时，请重试！')
            })
    })

});

