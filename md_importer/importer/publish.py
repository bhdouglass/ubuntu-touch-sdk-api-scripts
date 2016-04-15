from md_importer.importer import (
    DEFAULT_LANG,
    DEFAULT_TEMPLATE,
)
from md_importer.importer.tools import remove_leading_and_trailing_slash

from cms.api import create_page, add_plugin
from cms.models import Page, Title
from cms.utils.page_resolver import get_page_from_path
from djangocms_text_ckeditor.html import clean_html

from bs4 import BeautifulSoup
import logging
import re
import os


class ParentNotFoundException(Exception):
    def __init__(self, parent_url):
        self.parent_url = parent_url

    def __str__(self):
        return repr(self.parent_url)


class ArticlePage:
    def update(self, title, full_url, menu_title=None, in_navigation=True,
               html=None, template=None):
        if self.draft.get_title() != title:
            self.draft.title = title
        if self.draft.get_menu_title() != menu_title:
            self.draft.menu_title = menu_title
        if self.draft.in_navigation != in_navigation:
            self.draft.in_navigation = in_navigation
        if self.draft.template != template:
            self.draft.template = template
        if html:
            update = True
            if self.draft_text_plugin:
                if _compare_html(html, self.draft_text_plugin.body):
                    update = False
                elif self.text_plugin:
                        if _compare_html(html, self.text_plugin.body):
                            update = False
                if update:
                    self.draft_text_plugin.body = html
                    self.draft_text_plugin.save()
                else:
                    # Reset draft
                    self.draft.revert(DEFAULT_LANG)
            else:
                self.draft_plugin = add_plugin(
                    self.draft_placeholder, 'RawHtmlPlugin', DEFAULT_LANG,
                    body=html)

    def __init__(self, title, full_url, menu_title=None, in_navigation=True,
                 html=None, template=DEFAULT_TEMPLATE):
        self.page = None
        self.draft = None
        self.draft_placeholder = None
        self.draft_text_plugin = None

        # First check if pages already exist.
        drafts = Title.objects.select_related('page').filter(
            path__regex=full_url).filter(publisher_is_draft=True)
        if drafts:
            self.draft = drafts[0].page
        else:
            parent = _find_parent(full_url)
            if not parent:
                raise ParentNotFoundException(
                    'Parent for {} not found.'.format(full_url))
            slug = os.path.basename(full_url)
            self.draft = create_page(
                title=title, template=template, language=DEFAULT_LANG,
                slug=slug, parent=parent, menu_title=menu_title,
                in_navigation=in_navigation, position='last-child')
        (self.draft_placeholder,
         self.draft_plugin) = get_text_plugin(self.draft)
        self.update(title, full_url, menu_title, in_navigation, html,
                    template)

    def publish(self):
        if self.draft.is_dirty(DEFAULT_LANG):
            self.draft.publish(DEFAULT_LANG)
        if self.draft.get_public_object():
            self.page = self.draft.get_public_object()


def _compare_html(html_a, html_b):
    soup_a = BeautifulSoup(html_a, 'html5lib')
    soup_b = BeautifulSoup(html_b, 'html5lib')
    return (clean_html(soup_a.prettify()) == clean_html(soup_b.prettify()))


def slugify(filename):
    return os.path.basename(filename).replace('.md', '').replace('.html', '')


def _find_parent(full_url):
    parent_url = remove_leading_and_trailing_slash(re.sub(
        r'^\/None|{}\/'.format(DEFAULT_LANG),
        '',
        os.path.dirname(full_url)))
    parent_url = os.path.dirname(full_url)
    if not parent_url:
        root = Page.objects.get_home()
        if not root:
            return None
        return root
    parent = get_page_from_path(parent_url, draft=True)
    if not parent:
        logging.error('Parent {} not found.'.format(parent_url))
        return None
    return parent


def get_text_plugin(page):
    '''Finds text plugin, creates it if necessary.'''
    if not page:
        return (None, None)
    placeholders = page.placeholders.all()
    if not placeholders:
        return (None, None)
    # We create the page, so we know there's just one placeholder
    plugins = placeholders[0].get_plugins()
    if plugins:
        return (placeholders[0], plugins[0].get_plugin_instance()[0])
    plugin = add_plugin(
        placeholders[0], 'RawHtmlPlugin', DEFAULT_LANG,
        body='')
    return (placeholders[0], plugin)
