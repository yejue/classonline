$(()=>{
    // 上传封面图片
     // 上传文件input
    let $fileInput = $('.input-group-btn input');
    let $uploadBtn = $('.input-group-btn button');

    $uploadBtn.click(()=>{
        $fileInput.click()
    })

    // 自动上传
    $fileInput.change(function () {
        $this = $(this);
        // 只要文件input内容不为空，也就是选择了文件
        if ($this.val() !== ''){
            // 上传
            // 新建一个formdata对象
            let formData = new FormData();
            formData.append('upload', $this[0].files[0]);
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());

            $
                .ajax({
                    url: '/admin/upload/',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false
                })
                .done((res)=>{
                    if (res.data.uploaded === '1'){
                        message.showSuccess(res.errmsg);
                        // 把封面字段内容，改成上传的图片的url
                        $('input[name="image_url"]').val(res.data.url);
                        // 清空一下file input
                        $this.val('')
                    }else{
                        message.showError(res.errmsg)
                    }
                })
                .fail(()=>{
                    message.showError('服务器超时, 请重新尝试！')
                })
        }
    });

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
    // 保存
    $('.box-footer button.save').click(function () {
        // 更新富文本编辑器内容到form表单
        window.CKEDITOR.instances.id_content.updateElement();
        $
            .ajax({
                url: $(this).data('url'),
                data: $('form').serialize(),
                type: $(this).data('type')
            })
            .done((res) => {
                if (res['error'] === '0') {
                    message.showSuccess(res.errmsg);
                    $('#content').load(
                        $('.sidebar-menu li.active a').data('url'),
                        (response, status, xhr) => {
                            if (status !== 'success') {
                                message.showError('服务器超时，请重试！')
                            }
                        }
                    );
                } else if (res['error']==='4105'){
                    message.showError('您没有权限！')
                } else{
                    $('#content').html(res)
                }
            })
            .fail((res) => {
                message.showError('服务器超时，请重试！')
            })
    })
});