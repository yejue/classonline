from django.db import models


class BaseModel(models.Model):

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_delete = models.BooleanField('逻辑删除', default=False)

    class Meta:
        # 抽象类
        abstract = True

