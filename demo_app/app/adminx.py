from xadmin import views, sites, filters
from .models import IDC, Host, MaintainLog, HostGroup, AccessRecord
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction


class MainDashboard(object):
    # 只有禁止自定义才会使用通用方式
    widget_customiz = False

    widgets = [
        [
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3>"},
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count',
             'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {'o': '-guarantee_date'}},
            {"type": "dict_chart", "model": "app.idc", 'title': 'idc_day_count', 'chart': 'idc_count'},
        ],
        [
            {"type": "qbutton", "title": "Quick Start",
             "btns": [{'model': Host}, {'model': IDC}, {'title': "Google", 'url': "http://www.google.com"}]},
            {"type": "addform", "model": MaintainLog},
        ]
    ]


sites.site.register(views.website.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


sites.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    global_search_models = [Host, IDC]
    global_models_icon = {
        Host: 'fa fa-laptop', IDC: 'fa fa-cloud'
    }
    menu_style = 'default'  # 'accordion'


sites.site.register(views.CommAdminView, GlobalSetting)


class MaintainInline(object):
    model = MaintainLog
    extra = 1
    style = 'accordion'


def summary_idc_day_add():
    from django.db import connection
    from django.db.models import Count

    select = {'day': connection.ops.date_trunc_sql('day', 'create_time')}
    summary_dict = IDC.objects.extra(select=select).values('day').order_by("create_time") \
        .annotate(count=Count('id')).values_list("day", "count")
    return list(summary_dict)


class IDCAdmin(object):
    list_display = ('name', 'description', 'create_time')
    list_display_links = ('name',)
    wizard_form_list = [
        ('First\'s Form', ('name', 'description')),
        ('Second Form', ('contact', 'telphone', 'address')),
        ('Thread Form', ('customer_id',))
    ]

    search_fields = ['name']
    relfield_style = 'fk-select'
    reversion_enable = True

    actions = [BatchChangeAction, ]
    batch_fields = ('contact', 'groups')

    data_dict_charts = {
        "idc_count": {
            'title': u"IDC DAY COUNT",
            "x-field-name": "x",
            "y-field-name": "y",
            'datas': [{
                'data': summary_idc_day_add(),
                'label': "COUNT",
            }]
        },
    }


class HostAdmin(object):
    def open_web(self, instance):
        return "<a href='http://%s' target='_blank'>Open</a>" % instance.ip

    open_web.short_description = "Acts"
    open_web.allow_tags = True
    open_web.is_column = True

    list_display = ('name', 'idc', 'guarantee_date', 'service_type',
                    'status', 'open_web', 'description')
    list_display_links = ('name',)

    raw_id_fields = ('idc',)
    style_fields = {'system': "radio-inline"}

    search_fields = ['name', 'ip', 'description']
    list_filter = ['idc', 'guarantee_date', 'status', 'brand', 'model', 'cpu', 'core_num', 'hard_disk', 'memory',
                   ('service_type', filters.MultiSelectFieldListFilter)]

    list_quick_filter = ['service_type', {'field': 'idc__name', 'limit': 10}]
    list_bookmarks = [{'title': "Need Guarantee", 'query': {'status__exact': 2}, 'order': ('-guarantee_date',),
                       'cols': ('brand', 'guarantee_date', 'service_type')}]

    show_detail_fields = ('idc',)
    list_editable = (
        'name', 'idc', 'guarantee_date', 'service_type', 'description')
    save_as = True

    aggregate_fields = {"guarantee_date": "min"}
    grid_layouts = ('table', 'thumbnails')

    form_layout = (
        Main(
            TabHolder(
                Tab('Comm Fields',
                    Fieldset('Company data',
                             'name', 'idc',
                             description="some comm fields, required"
                             ),
                    Inline(MaintainLog),
                    ),
                Tab('Extend Fields',
                    Fieldset('Contact details',
                             'service_type',
                             Row('brand', 'model'),
                             Row('cpu', 'core_num'),
                             Row(AppendedText(
                                 'hard_disk', 'G'), AppendedText('memory', "G")),
                             'guarantee_date'
                             ),
                    ),
            ),
        ),
        Side(
            Fieldset('Status data',
                     'status', 'ssh_port', 'ip'
                     ),
        )
    )
    inlines = [MaintainInline]
    reversion_enable = True

    data_charts = {
        "host_service_type_counts": {
            'title': u"Host service type count", "x-field": "service_type",
            "y-field": ("service_type",),
            "option": {
                "series": {"bars": {"align": "center", "barWidth": 0.8, 'show': True}},
                "xaxis": {"aggregate": "count", "mode": "categories"},
            },
        },
    }


class HostGroupAdmin(object):
    list_display = ('name', 'description')
    list_display_links = ('name',)

    search_fields = ['name']
    style_fields = {'hosts': 'checkbox-inline'}


class MaintainLogAdmin(object):
    list_display = (
        'host', 'maintain_type', 'hard_type', 'time', 'operator', 'note')
    list_display_links = ('host',)

    list_filter = ['host', 'maintain_type', 'hard_type', 'time', 'operator']
    search_fields = ['note']

    form_layout = (
        Col("col2",
            Fieldset('Record data',
                     'time', 'note',
                     css_class='unsort short_label no_title'
                     ),
            span=9, horizontal=True
            ),
        Col("col1",
            Fieldset('Comm data',
                     'host', 'maintain_type'
                     ),
            Fieldset('Maintain details',
                     'hard_type', 'operator'
                     ),
            span=3
            )
    )
    reversion_enable = True


class AccessRecordAdmin(object):
    def avg_count(self, instance):
        return int(instance.view_count / instance.user_count)

    avg_count.short_description = "Avg Count"
    avg_count.allow_tags = True
    avg_count.is_column = True

    list_display = ('date', 'user_count', 'view_count', 'avg_count')
    list_display_links = ('date',)

    list_filter = ['date', 'user_count', 'view_count']
    actions = None
    aggregate_fields = {"user_count": "sum", 'view_count': "sum"}

    refresh_times = (3, 5, 10)
    data_charts = {
        "user_count": {'title': u"User Report", "x-field": "date", "y-field": ("user_count", "view_count"),
                       "order": ('date',)},
        "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)},
        "per_month": {'title': u"Monthly Users", "x-field": "_chart_month", "y-field": ("user_count",),
                      "option": {
                          "series": {"bars": {"align": "center", "barWidth": 0.8, 'show': True}},
                          "xaxis": {"aggregate": "sum", "mode": "categories"}, },
                      },
    }

    def _chart_month(self, obj):
        return obj.date.strftime("%B")


sites.site.register(Host, HostAdmin)
sites.site.register(HostGroup, HostGroupAdmin)
sites.site.register(MaintainLog, MaintainLogAdmin)
sites.site.register(IDC, IDCAdmin)
sites.site.register(AccessRecord, AccessRecordAdmin)
