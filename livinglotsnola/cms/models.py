from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent


class CollapsibleSectionContent(RichTextContent):

    title = models.CharField(_('title'), max_length=200)
    start_collapsed = models.BooleanField(_('start collapsed'), default=False)

    class Meta:
        abstract = True
        verbose_name = _('collapsible section')
        verbose_name_plural = _('collapsible sections')

    def render(self, **kwargs):
        return render_to_string('cms/collapsiblesection/default.html',
            { 'content': self }, context_instance=kwargs.get('context'))


class RecentActivitiesContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('recent activity list')
        verbose_name_plural = _('recent activity lists')

    def render(self, **kwargs):
        return render_to_string([
            'activity/plugin.html',
        ], {}, context_instance=kwargs.get('context'))


Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',

    'pagepermissions.extension',
)

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer', _('Footer'), 'inherited'),
    ),
})

Page.register_templates({
    'title': _('Map template'),
    'path': 'map.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer', _('Footer'), 'inherited'),
    ),
})

Page.create_content_type(RichTextContent)

Page.create_content_type(CollapsibleSectionContent)
Page.create_content_type(RecentActivitiesContent)

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('livinglots_lots.map_urls', _('Lots map')),
    ('elephantblog.urls', _('Blog')),
    ('extraadmin.cms_urls', _('Extra admin functions')),
    ('contact_form', _('Contact form'), {
        'urls': 'contact.form_urls',
    }),
    ('contact_success', _('Contact success'), {
        'urls': 'contact.success_urls',
    }),
))
