from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from developer_portal.views import login_failure

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'django_openid_auth.views',
    url(r'^openid/login/$', 'login_begin', name='openid-login',
        kwargs={'render_failure': login_failure}),
    url(r'^openid/complete/$', 'login_complete', name='openid-complete',
        kwargs={'render_failure': login_failure}),
    url(r'^openid/logo.gif$', 'logo', name='openid-logo'),
)

urlpatterns += i18n_patterns('',
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^blog/entries/', include('zinnia.urls', namespace='zinnia')),
    url(r'^blog/comments/', include('django_comments.urls')),
    url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

