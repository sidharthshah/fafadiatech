# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Customer.alfreduser_ptr'
        db.delete_column('alfredapp_customer', 'alfreduser_ptr_id')

        # Adding field 'Customer.user_ptr'
        db.add_column('alfredapp_customer', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'Customer.name'
        db.add_column('alfredapp_customer', 'name',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=100),
                      keep_default=False)

        # Deleting field 'Team.alfreduser_ptr'
        db.delete_column('alfredapp_team', 'alfreduser_ptr_id')

        # Deleting field 'Team.email'
        db.delete_column('alfredapp_team', 'email')

        # Adding field 'Team.user_ptr'
        db.add_column('alfredapp_team', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'Team.usertype'
        db.add_column('alfredapp_team', 'usertype',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=30),
                      keep_default=False)

        # Adding field 'Team.deparment'
        db.add_column('alfredapp_team', 'deparment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Deparment']),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Customer.alfreduser_ptr'
        db.add_column('alfredapp_customer', 'alfreduser_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['alfredapp.Alfreduser'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Customer.user_ptr'
        db.delete_column('alfredapp_customer', 'user_ptr_id')

        # Deleting field 'Customer.name'
        db.delete_column('alfredapp_customer', 'name')

        # Adding field 'Team.alfreduser_ptr'
        db.add_column('alfredapp_team', 'alfreduser_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['alfredapp.Alfreduser'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'Team.email'
        db.add_column('alfredapp_team', 'email',
                      self.gf('django.db.models.fields.EmailField')(default=0, max_length=75),
                      keep_default=False)

        # Deleting field 'Team.user_ptr'
        db.delete_column('alfredapp_team', 'user_ptr_id')

        # Deleting field 'Team.usertype'
        db.delete_column('alfredapp_team', 'usertype')

        # Deleting field 'Team.deparment'
        db.delete_column('alfredapp_team', 'deparment_id')

    models = {
        'alfredapp.alfreduser': {
            'Meta': {'object_name': 'Alfreduser', '_ormbases': ['auth.User']},
            'deparment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['alfredapp.Deparment']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'})
        },
        'alfredapp.customer': {
            'Meta': {'object_name': 'Customer', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'alternateemail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'alternatemobile': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'landline': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
            'Meta': {'object_name': 'Team', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'deparment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['alfredapp.Deparment']"}),
            'landlineno': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mobileno': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'})
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