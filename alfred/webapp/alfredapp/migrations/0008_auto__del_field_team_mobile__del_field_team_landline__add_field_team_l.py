# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Team.mobile'
        db.delete_column('alfredapp_team', 'mobile')

        # Deleting field 'Team.landline'
        db.delete_column('alfredapp_team', 'landline')

        # Adding field 'Team.landlineno'
        db.add_column('alfredapp_team', 'landlineno',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 5, 4, 0, 0), max_length=15),
                      keep_default=False)

        # Adding field 'Team.mobileno'
        db.add_column('alfredapp_team', 'mobileno',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 5, 4, 0, 0), max_length=11),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Team.mobile'
        db.add_column('alfredapp_team', 'mobile',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 5, 4, 0, 0), max_length=11),
                      keep_default=False)

        # Adding field 'Team.landline'
        db.add_column('alfredapp_team', 'landline',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 5, 4, 0, 0), max_length=15),
                      keep_default=False)

        # Deleting field 'Team.landlineno'
        db.delete_column('alfredapp_team', 'landlineno')

        # Deleting field 'Team.mobileno'
        db.delete_column('alfredapp_team', 'mobileno')

    models = {
        'alfredapp.alfreduser': {
            'Meta': {'object_name': 'Alfreduser', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'alfredapp.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'alternateemail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'alternatemobile': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landline': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'alfredapp.customerpackage': {
            'Meta': {'object_name': 'CustomerPackage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alfredapp.deparment': {
            'Meta': {'object_name': 'Deparment'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'alfredapp.dsk': {
            'Meta': {'object_name': 'Dsk'},
            'dsktype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'alfredapp.make': {
            'Meta': {'object_name': 'Make'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alfredapp.sla': {
            'Meta': {'object_name': 'Sla'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slatype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alfredapp.team': {
            'Meta': {'object_name': 'Team'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landlineno': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mobileno': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alfredapp.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'assignedto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Team']"}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Customer']"}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Deparment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Make']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.CustomerPackage']"}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'sla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Sla']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.TicketStatus']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ticketid': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {})
        },
        'alfredapp.ticketstatus': {
            'Meta': {'object_name': 'TicketStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'statustype': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['alfredapp']