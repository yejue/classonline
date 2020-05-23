from django.db import models

from utils.models import BaseModel

# Create your models here.


class Tag(BaseModel):
    """
    文章分类标签模型
    """
    name = models.CharField('标签名', max_length=64, help_text='标签名')

    class Meta:
        ordering = ['-update_time', '-id']  # 排序
        db_table = 'tb_tag'
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(BaseModel):
    """
    文章模型
    """
    title = models.CharField('标题', max_length=150, help_text='标题')
    digest = models.CharField('摘要', max_length=200, help_text='摘要')
    content = models.TextField('内容', help_text='内容')
    clicks = models.IntegerField('点击量', default=0, help_text='点击量')
    image_url = models.URLField('图片url', default='', help_text='图片url')

    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)

    author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-update_time', '-id']  # 排序
        db_table = 'tb_news'
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comments(BaseModel):
    """
    评论模型
    """
    content = models.TextField('内容', help_text='内容')
    author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time', '-id']  # 排序
        db_table = 'tb_comments'
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<评论 {}>'.format(self.id)


class HotNews(BaseModel):
    """
    推荐文章表
    """
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    priority = models.IntegerField('优先级', help_text='优先级')

    class Meta:
        ordering = ['-update_time', '-id']  # 排序
        db_table = 'tb_hotnews'
        verbose_name = "热门文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<热门新闻{}>'.format(self.id)


class Banner(BaseModel):
    """
    轮播图
    """
    image_url = models.URLField('图片url', default='', help_text='图片url')
    priority = models.IntegerField('优先级', help_text='优先级')

    news = models.OneToOneField('News', on_delete=models.CASCADE)

    class Meta:
        ordering = ['priority', '-update_time', '-id']  # 排序
        db_table = 'tb_banner'
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<轮播图{}>'.format(self.id)
