# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lot'
        db.create_table(u'lots_lot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['owners.Owner'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('known_use', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinglots_lots.Use'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('known_use_certainty', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('known_use_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('steward_inclusion_opt_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('polygon_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2, blank=True)),
            ('polygon_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lots.LotGroup'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'lots', ['Lot'])

        # Adding model 'LotGroup'
        db.create_table(u'lots_lotgroup', (
            (u'baselotgroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['livinglots_lots.BaseLotGroup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'lots', ['LotGroup'])


    def backwards(self, orm):
        # Deleting model 'Lot'
        db.delete_table(u'lots_lot')

        # Deleting model 'LotGroup'
        db.delete_table(u'lots_lotgroup')


    models = {
        u'livinglots_lots.baselotgroup': {
            'Meta': {'object_name': 'BaseLotGroup'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'known_use': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinglots_lots.Use']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'known_use_certainty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'known_use_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['owners.Owner']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'polygon_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'polygon_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'steward_inclusion_opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'livinglots_lots.use': {
            'Meta': {'object_name': 'Use'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'livinglots_owners.alias': {
            'Meta': {'object_name': 'Alias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lots.LotGroup']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'known_use': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinglots_lots.Use']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'known_use_certainty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'known_use_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['owners.Owner']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'polygon_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'polygon_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'steward_inclusion_opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'lots.lotgroup': {
            'Meta': {'object_name': 'LotGroup', '_ormbases': [u'livinglots_lots.BaseLotGroup']},
            u'baselotgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['livinglots_lots.BaseLotGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['livinglots_owners.Alias']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '20'})
        }
    }

    complete_apps = ['lots']