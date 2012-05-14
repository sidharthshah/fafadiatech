# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Deparment'
        db.delete_table('alfredapp_deparment')

        # Adding model 'Department'
        db.create_table('alfredapp_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('alfredapp', ['Department'])

        # Deleting field 'Alfreduser.deparment'
        db.delete_column('alfredapp_alfreduser', 'deparment_id')

        # Adding field 'Alfreduser.department'
        db.add_column('alfredapp_alfreduser', 'department',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Department']),
                      keep_default=False)

        # Deleting field 'Team.deparment'
        db.delete_column('alfredapp_team', 'deparment_id')

        # Adding field 'Team.department'
        db.add_column('alfredapp_team', 'department',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Department']),
                      keep_default=False)

        # Deleting field 'Ticket.make'
        db.delete_column('alfredapp_ticket', 'make_id')

        # Deleting field 'Ticket.priority'
        db.delete_column('alfredapp_ticket', 'priority')

        # Adding field 'Ticket.systemid'
        db.add_column('alfredapp_ticket', 'systemid',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=255),
                      keep_default=False)


        # Changing field 'Ticket.dept'
        db.alter_column('alfredapp_ticket', 'dept_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Department']))
    def backwards(self, orm):
        # Adding model 'Deparment'
        db.create_table('alfredapp_deparment', (
            ('department', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('alfredapp', ['Deparment'])

        # Deleting model 'Department'
        db.delete_table('alfredapp_department')

        # Adding field 'Alfreduser.deparment'
        db.add_column('alfredapp_alfreduser', 'deparment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Deparment']),
                      keep_default=False)

        # Deleting field 'Alfreduser.department'
        db.delete_column('alfredapp_alfreduser', 'department_id')

        # Adding field 'Team.deparment'
        db.add_column('alfredapp_team', 'deparment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Deparment']),
                      keep_default=False)

        # Deleting field 'Team.department'
        db.delete_column('alfredapp_team', 'department_id')

        # Adding field 'Ticket.make'
        db.add_column('alfredapp_ticket', 'make',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['alfredapp.Make']),
                      keep_default=False)

        # Adding field 'Ticket.priority'
        db.add_column('alfredapp_ticket', 'priority',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=11),
                      keep_default=False)

        # Deleting field 'Ticket.systemid'
        db.delete_column('alfredapp_ticket', 'systemid')


        # Changing field 'Ticket.dept'
        db.alter_column('alfredapp_ticket', 'dept_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Deparment']))
    models = {
        'alfredapp.alfreduser': {
            'Meta': {'object_name': 'Alfreduser', '_ormbases': ['auth.User']},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['alfredapp.Department']"}),
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
        'alfredapp.department': {
            'Meta': {'object_name': 'Department'},
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
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['alfredapp.Department']"}),
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
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.CustomerPackage']"}),
            'sla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Sla']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.TicketStatus']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'systemid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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