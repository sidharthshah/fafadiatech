# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Department'
        db.create_table('alfredapp_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('alfredapp', ['Department'])

        # Adding model 'Alfreduser'
        db.create_table('alfredapp_alfreduser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('usertype', self.gf('django.db.models.fields.CharField')(default=None, max_length=30)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['alfredapp.Department'])),
        ))
        db.send_create_signal('alfredapp', ['Alfreduser'])

        # Adding model 'TicketStatus'
        db.create_table('alfredapp_ticketstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statustype', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('alfredapp', ['TicketStatus'])

        # Adding model 'Team'
        db.create_table('alfredapp_team', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('usertype', self.gf('django.db.models.fields.CharField')(default=None, max_length=30)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['alfredapp.Department'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('landlineno', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('mobileno', self.gf('django.db.models.fields.CharField')(max_length=11)),
        ))
        db.send_create_signal('alfredapp', ['Team'])

        # Adding model 'Customer'
        db.create_table('alfredapp_customer', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('landline', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('alternatemobile', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('alternateemail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('alfredapp', ['Customer'])

        # Adding model 'CustomerPackage'
        db.create_table('alfredapp_customerpackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alfredapp', ['CustomerPackage'])

        # Adding model 'Sla'
        db.create_table('alfredapp_sla', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slatype', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alfredapp', ['Sla'])

        # Adding model 'Dsk'
        db.create_table('alfredapp_dsk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dsktype', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alfredapp', ['Dsk'])

        # Adding model 'Make'
        db.create_table('alfredapp_make', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alfredapp', ['Make'])

        # Adding model 'Ticket'
        db.create_table('alfredapp_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.DateTimeField')()),
            ('ticketid', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Customer'])),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Department'], null=True, blank=True)),
            ('systemid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.TicketStatus'], null=True, blank=True)),
            ('assignedto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Team'], null=True, blank=True)),
            ('sla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.Sla'], null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alfredapp.CustomerPackage'], null=True, blank=True)),
        ))
        db.send_create_signal('alfredapp', ['Ticket'])

    def backwards(self, orm):
        # Deleting model 'Department'
        db.delete_table('alfredapp_department')

        # Deleting model 'Alfreduser'
        db.delete_table('alfredapp_alfreduser')

        # Deleting model 'TicketStatus'
        db.delete_table('alfredapp_ticketstatus')

        # Deleting model 'Team'
        db.delete_table('alfredapp_team')

        # Deleting model 'Customer'
        db.delete_table('alfredapp_customer')

        # Deleting model 'CustomerPackage'
        db.delete_table('alfredapp_customerpackage')

        # Deleting model 'Sla'
        db.delete_table('alfredapp_sla')

        # Deleting model 'Dsk'
        db.delete_table('alfredapp_dsk')

        # Deleting model 'Make'
        db.delete_table('alfredapp_make')

        # Deleting model 'Ticket'
        db.delete_table('alfredapp_ticket')

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
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['alfredapp.Department']", 'null': 'True', 'blank': 'True'}),
            'landlineno': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mobileno': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'})
        },
        'alfredapp.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'assignedto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Team']", 'null': 'True', 'blank': 'True'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Customer']"}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Department']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.CustomerPackage']", 'null': 'True', 'blank': 'True'}),
            'sla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.Sla']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alfredapp.TicketStatus']", 'null': 'True', 'blank': 'True'}),
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