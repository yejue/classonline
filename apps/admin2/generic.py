from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.http import QueryDict
from django.views import View
from django.shortcuts import render

from utils.genJsonResponse import json_response


class TemplateView(View):
    """
    模板视图
    """
    model = None  # 模型
    template_name = None
    page_header = None  # 页头大标题
    page_option = None  # 页头小标题
    table_title = None  # 内容标题
    fields = None  # 需要展示的字段

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.get_template_name(), context=context)

    def get_context_data(self, **kwargs):
        context = {
            'page_header': self.page_header,
            'page_option': self.page_option,
            'table_title': self.table_title
        }

        context.update(kwargs)
        return context

    def get_template_name(self):
        """获取模板名"""
        if self.template_name is None:
            if isinstance(self, MyListView):
                self.template_name = 'admin/{0}/{0}_list.html'.format(self.model._meta.model_name)
            else:
                self.template_name = 'admin/{0}/{0}_detail.html'.format(self.model._meta.model_name)
        return self.template_name


class DetailView(View):
    """
    详情视图
    """
    form_class = None

    def get_form_class(self):
        """获取模型表单类"""
        if self.form_class is None:
            if self.fields is None:
                raise ImproperlyConfigured('未设置form或field字段')
            return modelform_factory(self.model, fields=self.fields)
        else:
            return self.form_class

    def save(self, form):
        form.save()


class MyListView(TemplateView):
    """
    通用对象列表视图
    """
    is_paginate = False  # 是否分页
    per_page = None  # 每页条数

    def get_context_data(self, **kwargs):
        """获取上下文变量，如果要添加额外变量，请复写此方法"""
        # 1. 获取查询集
        queryset = self.get_queryset()
        # 2. 分页
        if self.is_paginate:
            page_size = self.per_page
            if page_size:
                page = self.paginate_queryset(queryset, page_size)
            else:
                page = self.paginate_queryset(queryset, 10)
        else:
            page = queryset

        context = super().get_context_data(page_obj=page)
        context.update(kwargs)
        return context

    def get_queryset(self):
        """获取查询集，如果需要过滤，请复写此方法"""
        # 1.获取所有查询集
        if self.model is not None:
            queryset = self.model.objects.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s 未指定models" % {
                    'cls': self.__class__.__name__
                }
            )
        # 2.选择字段
        if self.fields:
            queryset = queryset.only(*self.fields)

        return queryset

    def paginate_queryset(self, queryset, page_size):
        """如果需要，进行分页"""
        paginator = Paginator(queryset, page_size)

        try:
            page_num = int(self.request.GET.get('page', 1))
        except Exception as e:
            page_num = 1
        page = paginator.get_page(page_num)
        return page


class UpdateView(TemplateView, DetailView):
    """
    更新对象视图
    """
    pk = None  # url的路径参数名，默认pk 对象的pk字段

    def get(self, request, **kwargs):
        self.obj = self.get_obj(**kwargs)
        context = self.get_context_data()
        return render(request, self.get_template_name(), context=context)

    def put(self, request, **kwargs):
        # 1. 获取模型对象
        self.obj = self.get_obj(**kwargs)
        # 2. 获取参数，创建模型表单对象
        self.form_class = self.get_form_class()
        form = self.form_class(QueryDict(request.body), instance=self.obj)
        # 3. 校验
        if form.is_valid():
            self.save(form)
            return json_response(errmsg='修改数据成功！')
        else:
            # 4. 返回结果
            context = self.get_context_data(form=form)

            return render(request, self.get_template_name(), context=context)

    def get_obj(self, **kwargs):
        self.get_obj_id(**kwargs)
        if self.model is None:
            raise ImproperlyConfigured('没有设置模型')
        obj = self.model.objects.filter(pk=self.obj_id).first()
        if not obj:
            raise ObjectDoesNotExist('找不到pk=%s的对象' % self.obj_id)
        return obj

    def get_obj_id(self, **kwargs):
        """获取传递的主键"""
        if self.pk is None:
            self.obj_id = kwargs.get('pk')
        else:
            self.obj_id = kwargs.get(self.pk)

    def get_context_data(self, **kwargs):
        """获取上下文变量"""
        # 1. 获取表单类
        self.form_class = self.get_form_class()
        # 2. 创建表单对象
        form = self.form_class(instance=self.obj)
        # 3. 构造模板变量
        context = super().get_context_data(form=form)
        context.update(kwargs)
        return context

    def save(self, form):
        """保存对象"""
        if form.has_changed():
            instance = form.save(commit=False)
            instance.save(update_fields=form.changed_data)


class AddView(TemplateView, DetailView):

    def post(self, request):
        # 1. 获取post参数，创建一个模型表单对象
        self.form_class = self.get_form_class()
        form = self.form_class(request.POST)
        # 2.校验
        if form.is_valid():
            # 3. 返回校验结果
            self.save(form)
            return json_response(errmsg='添加数据成功！')
        else:
            context = self.get_context_data(form=form)

            return render(request, self.get_template_name(), context=context)

    def get_context_data(self, **kwargs):
        # 1. 创建一个模型表单
        form = self.get_form_class()
        # 2. 模板变量
        context = super().get_context_data(form=form)
        context.update(kwargs)
        return context