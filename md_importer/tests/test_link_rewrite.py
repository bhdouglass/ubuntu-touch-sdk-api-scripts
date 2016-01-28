from bs4 import BeautifulSoup

from cms.models import Page

from ..importer.article import Article
from .utils import (
    db_add_empty_page,
    is_local_link,
    TestLocalBranchImport,
)


class TestLinkRewrite(TestLocalBranchImport):
    def runTest(self):
        self.create_repo('data/link-test')
        self.repo.add_directive('', '')
        self.assertTrue(self.repo.execute_import_directives())
        self.assertTrue(self.repo.publish())
        pages = Page.objects.filter(publisher_is_draft=False)
        self.assertEqual(pages.count(), 1+2)  # root + 2 articles
        for article in self.repo.imported_articles:
            self.assertTrue(isinstance(article, Article))
            self.assertEqual(article.page.parent, self.root)
            soup = BeautifulSoup(article.html, 'html5lib')
            for link in soup.find_all('a'):
                page = self.check_local_link(link.attrs['href'])
                self.assertIsNotNone(
                    page,
                    msg='Link {} not found. Available pages: {}'.format(
                        link.attrs['href'],
                        ', '.join([p.get_absolute_url() for p in pages])))
                self.assertIn(page, pages)


class TestLinkBrokenRewrite(TestLocalBranchImport):
    def runTest(self):
        self.create_repo('data/link-broken-test')
        self.repo.add_directive('', '')
        self.assertTrue(self.repo.execute_import_directives())
        self.assertTrue(self.repo.publish())
        pages = Page.objects.filter(publisher_is_draft=False)
        self.assertEqual(pages.count(), 1+2)  # root + 2 articles
        for article in self.repo.imported_articles:
            self.assertTrue(isinstance(article, Article))
            self.assertEqual(article.page.parent, self.root)
            soup = BeautifulSoup(article.html, 'html5lib')
            for link in soup.find_all('a'):
                if link.has_attr('class') and \
                   'headeranchor-link' in link.attrs['class']:
                    break
                page = self.check_local_link(link.attrs['href'])
                self.assertIsNone(page)
                self.assertNotIn(page, pages)


class TestSnapcraftLinkRewrite(TestLocalBranchImport):
    def runTest(self):
        self.create_repo('data/snapcraft-test')
        snappy_page = db_add_empty_page('Snappy', self.root)
        self.assertFalse(snappy_page.publisher_is_draft)
        build_apps = db_add_empty_page('Build Apps', snappy_page)
        self.assertFalse(build_apps.publisher_is_draft)
        self.assertEqual(
            3, Page.objects.filter(publisher_is_draft=False).count())
        self.repo.add_directive('docs', 'snappy/build-apps/devel')
        self.repo.add_directive('README.md', 'snappy/build-apps/devel')
        self.repo.add_directive(
            'HACKING.md', 'snappy/build-apps/devel/hacking')
        self.assertTrue(self.repo.execute_import_directives())
        self.assertTrue(self.repo.publish())
        pages = Page.objects.all()
        for article in self.repo.imported_articles:
            self.assertTrue(isinstance(article, Article))
            self.assertGreater(len(article.html), 0)
        for article in self.repo.imported_articles:
            soup = BeautifulSoup(article.html, 'html5lib')
            for link in soup.find_all('a'):
                if not is_local_link(link):
                    break
                page = self.check_local_link(link.attrs['href'])
                self.assertIsNotNone(
                    page,
                    msg='Link {} not found. Available pages: {}'.format(
                        link.attrs['href'],
                        ', '.join([p.get_absolute_url() for p in pages])))
                self.assertIn(page, pages)