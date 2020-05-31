import logging
import json
from django.db.models import F
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseNotFound

from .models import Tag, News, HotNews, Banner, Comments
from .constants import *
from utils.res_code import Code, error_map
from utils.genJsonResponse import json_response

# Create your views here.

logger = logging.getLogger('django')


def index(request):
    """
    新闻首页视图
    :param request:
    :return:
    url: /
    """
    # 新闻标签
    tags = Tag.objects.filter(is_delete=False).only('name')
    hot_news = HotNews.objects.select_related('news').only('news__title', 'news__image_url', 'news_id')\
                   .filter(is_delete=False).order_by('priority', 'news__clicks')[:HOT_NEWS_COUNT]
    return render(request, 'news/index.html', context={
        'tags': tags,
        'hot_news': hot_news
    })


class NewsListView(View):
    """
    新闻列表视图
    url: news/news/
    """

    def get(self, request):
        # 获取数据
        try:
            tag_id = int(request.GET.get('tag_id', 0))
        except Exception as e:
            logger.error("标签错误：\n{}".format(e))
            tag_id = 0
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.error("当前页数错误：\n{}".format(e))
            page = 1

        # 获取查询集
        news_queryset = News.objects.values('id', 'title', 'digest', 'image_url', 'update_time').annotate(
            tag_name=F('tag__name'), author=F('author__username')
        )
        # news_queryset = News.objects.select_related('tag', 'author'). \
        #     only('title', 'digest', 'image_url', 'update_time', 'tag__name', 'author__username')

        news = news_queryset.filter(is_delete=False, tag_id=tag_id) or news_queryset.filter(is_delete=False)
        # 分页
        paginator = Paginator(news, PER_PAGE_NEWS_COUNT)
        # 获取当前页数据
        news_info = paginator.get_page(page)
        # 返回数据
        data = {
            'total_pages': paginator.num_pages,
            'news': list(news_info)
        }
        return json_response(data=data)


class NewsBannerView(View):
    """
    轮播图视图
    url: news/banners
    """
    def get(self, request):
        banners = Banner.objects.values('news_id')\
                      .annotate(news_title=F('news__title'), image_url=F('news__image_url'))\
                      .filter(is_delete=False)[:SHOW_BANNER_COUNT]
        data = {
            'banners': list(banners)
        }
        return json_response(data=data)


class NewsDetailView(View):
    """
    新闻详情页
    url: news/news/<int:news_id>
    """
    def get(self, request, news_id):
        # 校验，是否存在 获取数据
        # news = News.objects.select_related('tag', 'author'). \
        #     only('title', 'content', 'update_time', 'tag__name', 'author__username').\
        #     filter(is_delete=False, id=news_id).first()
        # 展示数据
        # if news:
        #     return render(request, 'news/news_detail.html', context={
        #         'news': news
        #     })
        # else:
        #     return HttpResponseNotFound('<h1>Page not found</h1>')

        news_queryset = News.objects.select_related('tag', 'author').\
            only('title', 'content', 'update_time', 'tag__name', 'author__username')
        news = get_object_or_404(news_queryset, is_delete=False, id=news_id)

        # 加载评论
        comments = Comments.objects.select_related('author', 'parent'). \
            only('content', 'author__username', 'update_time',
                 'parent__author__username', 'parent__content', 'parent__update_time'). \
            filter(is_delete=False, news_id=news_id)

        return render(request, 'news/news_detail.html', context={
            'news': news,
            'comments': comments
        })


class NewsCommentView(View):
    """
    新闻评论添加功能
    url: news/news/<int:news_id>/comment
    """
    def post(self, request, news_id):
        # 是否登录
        if not request.user.is_authenticated:
            return json_response(errorno=Code.SESSIONERR, errmsg=error_map[Code.SESSIONERR])
        # 新闻是否存在
        if not News.objects.only('id').filter(is_delete=False, id=news_id).exists():
            return json_response(errorno=Code.PARAMERR, errmsg="新闻不存在！")

        # 判断内容
        json_data = request.body
        if not json_data:
            return json_response(errorno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json_data 转换成json
        json_data = json.loads(json_data.decode('utf8'))
        # 判断内容是否为空
        content = json_data.get('content')
        if not content:
            return json_response(errorno=Code.PARAMERR, errmsg='评论内容不能为空')

        # 判断父id是否正常
        parent_id = json_data.get('parent_id')
        try:
            if parent_id:
                parent_id = int(parent_id)
                if not Comments.objects.only('id'). \
                        filter(is_delete=False, id=parent_id, news_id=news_id).exists():
                    return json_response(errorno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        except Exception as e:
            logger.info("前端传过来的parent_id异常：\n{}".format(e))
            return json_response(errorno=Code.PARAMERR, errmsg="未知异常")

        # 保存到数据库
        new_comment = Comments()
        new_comment.content = content
        new_comment.news_id = news_id
        new_comment.author = request.user
        new_comment.parent_id = parent_id if parent_id else None
        new_comment.save()

        # 序列化一个评论数据
        return json_response(data=new_comment.to_dict_data())


def search(request):
    return render(request, 'news/search.html')
