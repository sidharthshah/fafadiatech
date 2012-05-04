# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alfreduser'
        db.create_table('alfredapp_alfreduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usertype', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('alfredapp', ['Alfreduser'])

    def backwards(self, orm):
        # Deleting model 'Alfreduser'
        db.delete_table('alfredapp_alfreduser')

    models = {
        'alfredapp.alfreduser': {
            'Meta': {'object_name': 'Alfreduser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['alfredapp']