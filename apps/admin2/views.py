import logging
import os

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import QueryDict
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission, ContentType, Group

from .forms import MenuModelForm
from .generic import *
from news.models import *
from course.models import *
from doc.models import *
from .models import Menu
from .forms import UserModelForm, GroupModeForm, NewsModelForm
from user.models import *
from utils.genJsonResponse import json_response
from utils.res_code import Code, error_map
from utils.ck_uploader.funcs import get_filename
from .constants import ORDER_BY_GROUP_PER_PAGE_COUNT

logger = logging.getLogger('django')


class MyPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        """
        覆盖父类方法，解决不同请求，权限不同的问题。
        """
        perms = self.get_permission_required()
        if isinstance(perms, dict):
            if self.request.method.lower() in perms:
                return self.request.user.has_perms(perms[self.request.method.lower()])
        else:
            return self.request.user.has_perms(perms)

    def handle_no_permission(self):
        """
        覆盖父类方法，解决ajax返回json数据的问题
        :return:
        """
        if self.request.is_ajax():
            if self.request.user.is_authenticated:
                return json_response(errorno=Code.ROLEERR, errmsg='您没有权限！')
            else:
                return json_response(errorno=Code.SESSIONERR, errmsg=
                '您未登录，请登录！', data={'url': reverse(self.get_login_url())})
        else:
            return super().handle_no_permission()


class IndexView(View):
    """
    后台首页视图
    """

    def get(self, request):

        objs = Menu.objects.only('name', 'url', 'icon', 'permission__codename',
                                 'permission__content_type__app_label').select_related(
            'permission__content_type').filter(is_delete=False, is_visible=True, parent=None)
        has_permissions = request.user.get_all_permissions()
        menus = []
        for menu in objs:
            if '%s.%s' % (menu.permission.content_type.app_label, menu.permission.codename) in has_permissions:
                temp = {
                    'name': menu.name,
                    'icon': menu.icon
                }

                children = menu.children.filter(is_delete=False, is_visible=True)
                if children:
                    temp['children'] = []
                    for child in children:
                        if '%s.%s' % (
                        child.permission.content_type.app_label, child.permission.codename) in has_permissions:
                            temp['children'].append({
                                'name': child.name,
                                'url': child.url
                            })
                else:
                    if not menu.url:
                        continue
                    temp['url'] = menu.url
                menus.append(temp)
        return render(request, 'admin/index.html', context={'menus': menus})


class HomeView(View):
    """
    工作台视图
    """

    def get(self, request):
        return render(request, 'admin/home.html')


class WaitView(View):
    """
    未上线功能提示
    """

    def get(self, request):
        return render(request, 'admin/wait.html')


class MenuListView(MyPermissionRequiredMixin, View):
    """
    菜单列表视图
    url:/admin/menus/
    """
    permission_required = ('admin2.menu_list',)

    def get(self, request):
        menus = Menu.objects.only('name', 'url', 'icon', 'is_visible', 'order', 'codename').filter(is_delete=False,
                                                                                                   parent=None)

        return render(request, 'admin/menu/menu_list.html', context={'menus': menus})


class MenuAddView(MyPermissionRequiredMixin, View):
    """
    添加菜单视图
    url:/admin/menu/
    """
    permission_required = ('admin2.menu_add',)

    def get(self, request):
        form = MenuModelForm()
        return render(request, 'admin/menu/add_menu.html', context={'form': form})

    def post(self, request):
        form = MenuModelForm(request.POST)

        if form.is_valid():
            new_menu = form.save()
            content_type = ContentType.objects.filter(app_label='admin2', model='menu').first()
            permission = Permission.objects.create(name=new_menu.name, content_type=content_type,
                                                   codename=new_menu.codename)
            new_menu.permission = permission
            new_menu.save(update_fields=['permission'])
            return json_response(errmsg='菜单添加成功！')
        else:
            return render(request, 'admin/menu/add_menu.html', context={'form': form})


class MenuUpdateView(MyPermissionRequiredMixin, View):
    """
    菜单管理视图
    url:/admin/menu/<int:menu_id>/
    """
    permission_required = {
        'delete': ('admin2.menu_delete',),
        'put': ('admin2.menu_update',),
        'get': ('admin2.menu_update',),
    }

    def delete(self, request, menu_id):
        menu = Menu.objects.filter(id=menu_id).only('name')
        if menu:
            menu = menu[0]
            if menu.children.filter(is_delete=False).exists():
                return json_response(errorno=Code.DATAERR, errmsg='父菜单不能删除！')
            menu.permission.delete()
            return json_response(errmsg='删除菜单：%s成功' % menu.name)
        else:
            return json_response(errorno=Code.NODATA, errmsg='菜单不存在！')

    def get(self, request, menu_id):
        menu = Menu.objects.filter(id=menu_id).first()
        form = MenuModelForm(instance=menu)
        return render(request, 'admin/menu/update_menu.html', context={'form': form})

    def put(self, request, menu_id):
        menu = Menu.objects.filter(id=menu_id).first()
        put_data = QueryDict(request.body)
        form = MenuModelForm(put_data, instance=menu)
        if form.is_valid():
            obj = form.save()
            flag = False
            if 'name' in form.changed_data:
                obj.permission.name = obj.name
                flag = True
            if 'codename' in form.changed_data:
                obj.permission.codename = obj.name
                flag = True
            if flag:
                obj.permission.save()
            return json_response(errmsg='菜单修改成功！')
        else:
            return render(request, 'admin/menu/update_menu.html', context={'form': form})


class UserListView(View):
    """
    用户列表视图
    """

    permission_required = ('admin2.user_list',)

    def get(self, request):
        user_queryset = User.objects.only('username', 'is_active', 'mobile', 'is_staff', 'is_superuser')
        groups = Group.objects.only('name').all()
        query_dict = {}
        # 检索
        groups__id = request.GET.get('group')
        if groups__id:
            try:
                group_id = int(groups__id)
                query_dict['groups__id'] = groups__id
            except Exception as e:
                pass

        is_staff = request.GET.get('is_staff')
        if is_staff == '0':
            query_dict['is_staff'] = False
        if is_staff == '1':
            query_dict['is_staff'] = True

        is_superuser = request.GET.get('is_superuser')
        if is_superuser == '0':
            query_dict['is_superuser'] = False
        if is_superuser == '1':
            query_dict['is_superuser'] = True

        username = request.GET.get('username')

        if username:
            query_dict['username'] = username

        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1

        paginator = Paginator(user_queryset.filter(**query_dict), ORDER_BY_GROUP_PER_PAGE_COUNT)

        users = paginator.get_page(page)
        context = {
            'users': users,
            'groups': groups
        }
        context.update(query_dict)
        return render(request, 'admin/user/user_list.html', context=context)


class UserUpdateView(View):
    """
    用户更新视图
    url:/admin/user/<int:user_id>
    """
    permission_required = {
        'get': ('admin2.user_detail',),
        'put': ('admin2.user_update',)
    }

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            form = UserModelForm(instance=user)
        else:
            form = UserModelForm()
        return render(request, 'admin/user/user_detail.html', context={'form': form})

    def put(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        put = QueryDict(request.body)
        if user:
            form = UserModelForm(put, instance=user)
        else:
            form = UserModelForm()
        if form.is_valid():
            form.save()
            return json_response()
        else:
            return render(request, 'admin/user/user_detail.html', context={'form': form})


class GroupListView(View):
    """
    分组列表视图
    url:/admin/groups/
    """

    def get(self, request):
        groups = Group.objects.only('name').all()

        return render(request, 'admin/group/group_list.html', context={'groups': groups})


class GroupAddView(View):
    """
    添加分组视图
    url: /admin/group/
    """

    def get(self, request):
        # 1. 创建一个空表单
        form = GroupModeForm()
        # 2. 拿到所有的可用一级菜单
        menus = Menu.objects.only('name', 'permission_id').select_related('permission').filter(is_delete=False,
                                                                                               parent=None)
        # 3. 返回渲染表单
        return render(request, 'admin/group/group_detail.html', context={
            'form': form,
            'menus': menus
        })

    def post(self, request):
        # 1.根据post的数据，创建模型表单对象
        form = GroupModeForm(request.POST)
        # 2.校验
        if form.is_valid():
            # 3.如果成功，保存，返回ok
            form.save()
            return json_response(errmsg='添加分组成功！')
        else:
            # 4.如果失败，返回渲染了错误信息的表单html
            menus = Menu.objects.only('name', 'permission_id').select_related('permission').filter(is_delete=False,
                                                                                                   parent=None)
            return render(request, 'admin/group/group_detail.html', context={
                'form': form,
                'menus': menus
            })


class GroupUpdateView(View):
    """
    分组更新视图
    url:/admin/group/<int:group_id>/
    """

    def get(self, request, group_id):
        # 1. 拿到要修改的分组
        group = Group.objects.filter(id=group_id).first()
        # 1.1 判断是否存不存在
        if not group:
            return json_response(errorno=Code.NODATA, errmsg='没有此分组！')
        # 2.创建表单
        form = GroupModeForm(instance=group)
        # 3.拿到所有的可用一集菜单
        menus = Menu.objects.only('name', 'permission_id').select_related('permission').filter(is_delete=False,
                                                                                               parent=None)
        # 4.拿到当前组的可用权限
        permissions = group.permissions.only('id').all()
        # 3.返回渲染html
        return render(request, 'admin/group/group_detail.html', context={
            'form': form,
            'menus': menus,
            'permissions': permissions
        })

    def put(self, request, group_id):
        # 1. 拿到要修改的分组
        group = Group.objects.filter(id=group_id).first()
        # 1.1 判断是否存不存在
        # 1.1 判断是否存不存在
        if not group:
            return json_response(errorno=Code.NODATA, errmsg='没有此分组！')
        # 2. 拿到前端传递的参数
        put_data = QueryDict(request.body)
        # 3. 校验参数
        # 3.1 创建表单对象
        form = GroupModeForm(put_data, instance=group)
        if form.is_valid():
            # 4. 如果成功，保存数据
            form.save()
            return json_response(errmsg='修改分组成功！')
        else:
            # 5. 如果失败
            menus = Menu.objects.only('name', 'permission_id').select_related('permission').filter(is_delete=False,
                                                                                                   parent=None)
            # 4.拿到当前组的可用权限
            permissions = group.permissions.only('id').all()
            return render(request, 'admin/group/group_detail.html', context={
                'form': form,
                'menus': menus,
                'permissions': permissions
            })


class NewsAdminView(View):
    """
    新闻列表视图
    url:admin/newsadmin/
    """

    def get(self, request):
        queryset = News.objects.only('title', 'tag__name', 'author__username', 'is_delete').select_related('tag',
                                                                                                           'author').all()
        tags = Tag.objects.only('name').filter(is_delete=False)
        query_dict = {}

        tag_id = request.GET.get('tag')
        if tag_id:
            query_dict['tag_id'] = tag_id
            queryset = queryset.filter(tag_id=tag_id)

        title = request.GET.get('title')
        if title:
            query_dict['title'] = title
            queryset = queryset.filter(title__contains=title)
        is_delete = request.GET.get('is_delete', None)

        flag = False

        if is_delete == '0':
            is_delete = True
            flag = True

        if is_delete == '1':
            is_delete = False
            flag = True

        if flag:
            queryset = queryset.filter(is_delete=is_delete)

        query_dict['is_delete'] = is_delete

        paginator = Paginator(queryset, 10)

        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1

        newses = paginator.get_page(page)

        context = {
            'newses': newses,
            'tags': tags
        }

        context.update(query_dict)

        return render(request, 'admin/news/news_list.html', context=context)


class NewsUpdateView(View):
    """
    新闻修改视图
    url:/admin/news/<int:news_id>/
    """
    def get(self, request, news_id):
        # 1. 拿到对应的新闻对象
        news = News.objects.filter(id=news_id).first()
        if news:
            # 2. 生成表单对象
            form = NewsModelForm(instance=news)
        else:
            return json_response(errorno=Code.NODATA, errmsg='没有此新闻！')
        # 3. 渲染并返回
        return render(request, 'admin/news/news_detail.html', context={'form': form})

    def put(self, request, news_id):
        news = News.objects.filter(id=news_id).first()
        put = QueryDict(request.body)
        if news:
            form = NewsModelForm(put, instance=news)
        else:
            form = NewsModelForm()

        if form.is_valid():
            # 优化
            # form.save()
            if form.has_changed():
                instance = form.save(commit=False)
                instance.save(update_fields=form.changed_data)

            return json_response(errmsg='修改新闻成功！')
        else:

            return render(request, 'admin/news/news_detail.html', context={
                'form': form,
            })


class UploadFileView(View):
    """
    上传文件视图
    url:/admin/upload/
    """

    def post(self, request):
        try:
            file = request.FILES['upload']
            filename = get_filename(file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            return json_response(data={
                'url': settings.MEDIA_URL + filename,
                'name': filename,
                'uploaded': '1'
            })
        except Exception as e:
            return json_response(data={'uploaded': '0'})


class NewsAddView(View):
    """
    新闻添加视图
    """
    def get(self, request):
        form = NewsModelForm()
        return render(request, 'admin/news/news_detail.html', context={'form': form})

    def post(self, request):
        form = NewsModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return json_response(errmsg='添加新闻成功！')
        else:
            return render(request, 'admin/news/news_detail.html', context={'form': form})


class TagListView(MyPermissionRequiredMixin, MyListView):
    permission_required = ('admin2.news_tag_list', )
    model = Tag
    page_header = '系统设置'
    page_option = '新闻标签管理'
    table_title = '新闻标签列表'
    is_paginate = True

    fields = ['name', 'is_delete']


class TagUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = ('admin2.news_tag_update',)
    model = Tag

    page_header = '系统设置'
    page_option = '新闻标签管理'
    table_title = '新闻标签更新'

    fields = ['name', 'is_delete']
    pk = 'tag_id'


class TagAddView(MyPermissionRequiredMixin, AddView):
    permission_required = ('admin2.news_tag_add', )
    model = Tag

    page_header = '系统设置'
    page_option = '新闻标签管理'
    table_title = '新闻标签添加'

    fields = ['name', 'is_delete']


class HotNewsListView(MyPermissionRequiredMixin, MyListView):
    permission_required = ('admin2.hotnews_list',)
    model = HotNews
    page_header = '新闻管理'
    page_option = '热门新闻管理'
    table_title = '热门新闻列表'
    fields = ['news__title', 'news__tag__name', 'priority', 'is_delete']

    is_paginate = True
    per_page = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('news__tag').order_by('-priority')


class HotNewsUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = ('admin2.hotnews_update',)
    model = HotNews

    page_header = '新闻管理'
    page_option = '热门新闻管理'
    table_title = '热门新闻更新'
    fields = ['priority', 'is_delete']


class HotNewsAddView(MyPermissionRequiredMixin, AddView):
    permission_required = ('admin2.hotnews_add',)
    model = HotNews

    page_header = '新闻管理'
    page_option = '热门新闻管理'
    table_title = '热门新闻添加'
    fields = ['news', 'priority']



class BannerListView(MyPermissionRequiredMixin, MyListView):

    permission_required = ('admin2.banner_list',)
    model = Banner
    page_header = '新闻管理'
    page_option = '轮播图管理'
    table_title = '轮播图列表'

    fields = ['image_url', 'priority', 'news__title', 'news__tag__name', 'is_delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('news__tag').order_by('-priority')


class BannerUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = ('admin2.banner_update',)
    model = Banner
    page_header = '新闻管理'
    page_option = '轮播图管理'
    table_title = '轮播图更新'

    fields = ['image_url', 'priority', 'news', 'is_delete']


class BannerAddView(MyPermissionRequiredMixin, AddView):
    permission_required = ('admin2.banner_add',)
    model = Banner
    page_header = '新闻管理'
    page_option = '轮播图管理'
    table_title = '轮播图添加'

    fields = ['image_url', 'priority', 'news', 'is_delete']


class DocListView(MyPermissionRequiredMixin, MyListView):
    permission_required = ('admin2.doc_list',)
    model = Doc
    page_header = '文档管理'
    page_option = '文档管理'
    table_title = '文档列表'

    fields = ['title', 'desc', 'file_url', 'image_url', 'author__username', 'is_delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('author')


class DocUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = ('admin2.doc_update',)
    model = Doc
    page_header = '文档管理'
    page_option = '文档管理'
    table_title = '文档更新'

    fields = ['title', 'desc', 'file_url', 'image_url', 'author', 'is_delete']


class DocAddView(MyPermissionRequiredMixin, AddView):
    permission_required = ('admin2.doc_add',)
    model = Doc
    page_header = '文档管理'
    page_option = '文档管理'
    table_title = '文档添加'

    fields = ['title', 'desc', 'file_url', 'image_url', 'is_delete']

    def save(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()


class CourseListView(MyPermissionRequiredMixin, MyListView):
    permission_required = ('admin2.course_list',)
    model = Course
    page_header = '在线课堂'
    page_option = '课程管理'
    table_title = '课程列表'

    fields = ['title', 'category__name', 'teacher__name', 'profile', 'outline', 'duration', 'cover_url', 'is_delete']


class CourseUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = ('admin2.course_update',)
    model = Course
    page_header = '在线课堂'
    page_option = '课程管理'
    table_title = '课程更新'

    fields = ['title', 'category', 'teacher', 'profile', 'outline', 'duration', 'cover_url', 'video_url']


class CourseAddView(MyPermissionRequiredMixin, AddView):
    permission_required = ('admin2.course_add',)
    model = Course
    page_header = '在线课堂'
    page_option = '课程管理'
    table_title = '课程添加'

    fields = ['title', 'category', 'teacher', 'profile', 'outline', 'duration', 'cover_url', 'video_url']