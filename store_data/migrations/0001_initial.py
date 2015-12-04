# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Release'
        db.create_table(u'store_data_release', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'store_data', ['Release'])

        # Adding model 'Architecture'
        db.create_table(u'store_data_architecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'store_data', ['Architecture'])

        # Adding model 'ScreenshotURL'
        db.create_table(u'store_data_screenshoturl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'store_data', ['ScreenshotURL'])

        # Adding model 'GadgetSnap'
        db.create_table(u'store_data_gadgetsnap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ratings_average', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=1)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('store_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=5000)),
        ))
        db.send_create_signal(u'store_data', ['GadgetSnap'])

        # Adding M2M table for field release on 'GadgetSnap'
        m2m_table_name = db.shorten_name(u'store_data_gadgetsnap_release')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gadgetsnap', models.ForeignKey(orm[u'store_data.gadgetsnap'], null=False)),
            ('release', models.ForeignKey(orm[u'store_data.release'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gadgetsnap_id', 'release_id'])

        # Adding M2M table for field architecture on 'GadgetSnap'
        m2m_table_name = db.shorten_name(u'store_data_gadgetsnap_architecture')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gadgetsnap', models.ForeignKey(orm[u'store_data.gadgetsnap'], null=False)),
            ('architecture', models.ForeignKey(orm[u'store_data.architecture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gadgetsnap_id', 'architecture_id'])

        # Adding M2M table for field screenshot_url on 'GadgetSnap'
        m2m_table_name = db.shorten_name(u'store_data_gadgetsnap_screenshot_url')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gadgetsnap', models.ForeignKey(orm[u'store_data.gadgetsnap'], null=False)),
            ('screenshoturl', models.ForeignKey(orm[u'store_data.screenshoturl'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gadgetsnap_id', 'screenshoturl_id'])


    def backwards(self, orm):
        # Deleting model 'Release'
        db.delete_table(u'store_data_release')

        # Deleting model 'Architecture'
        db.delete_table(u'store_data_architecture')

        # Deleting model 'ScreenshotURL'
        db.delete_table(u'store_data_screenshoturl')

        # Deleting model 'GadgetSnap'
        db.delete_table(u'store_data_gadgetsnap')

        # Removing M2M table for field release on 'GadgetSnap'
        db.delete_table(db.shorten_name(u'store_data_gadgetsnap_release'))

        # Removing M2M table for field architecture on 'GadgetSnap'
        db.delete_table(db.shorten_name(u'store_data_gadgetsnap_architecture'))

        # Removing M2M table for field screenshot_url on 'GadgetSnap'
        db.delete_table(db.shorten_name(u'store_data_gadgetsnap_screenshot_url'))


    models = {
        u'store_data.architecture': {
            'Meta': {'object_name': 'Architecture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'store_data.gadgetsnap': {
            'Meta': {'object_name': 'GadgetSnap'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'architecture': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['store_data.Architecture']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '5000'}),
            'icon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ratings_average': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'release': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['store_data.Release']", 'symmetrical': 'False'}),
            'screenshot_url': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['store_data.ScreenshotURL']", 'symmetrical': 'False'}),
            'store_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'store_data.release': {
            'Meta': {'object_name': 'Release'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'store_data.screenshoturl': {
            'Meta': {'object_name': 'ScreenshotURL'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['store_data']