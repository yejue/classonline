from news.templatetags.news_template_filters import register


@ register.inclusion_tag('box/paginatorbox.html')
def paginator_box(page, query):
    return {
        'page': page,
        'query': query
}