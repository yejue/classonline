import logging
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import Tag, News
from .constants import *
from utils.genCheckJson import genCheckJson
from utils.res_code import Code, error_map
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
    return render(request, 'news/index.html', context={
        'tags': tags
    })


class NewsListView(View):
    """
    新闻列表视图
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
        return JsonResponse(genCheckJson(data=data))


def search(request):
    return render(request, 'news/search.html')
