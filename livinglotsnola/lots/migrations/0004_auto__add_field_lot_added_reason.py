# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lot.added_reason'
        db.add_column(u'lots_lot', 'added_reason',
                      self.gf('django.db.models.fields.CharField')(default='no reason', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lot.added_reason'
        db.delete_column(u'lots_lot', 'added_reason')


    models = {
        u'livinglots_lots.baselotgroup': {
            'Meta': {'object_name': 'BaseLotGroup'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_reason': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
            'added_reason': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
            'parcel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parcels.Parcel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'polygon_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'polygon_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'steward_inclusion_opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'lots.lotgroup': {
            'Meta': {'object_name': 'LotGroup', '_ormbases': [u'livinglots_lots.BaseLotGroup']},
            u'baselotgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['livinglots_lots.BaseLotGroup']", 'unique': 'True', 'primary_key': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lots.LotGroup']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['livinglots_owners.Alias']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '20'})
        },
        u'parcels.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'acres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'geopin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hectares': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'objectid_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'perimeter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shape_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shape_len': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'situs_dir': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'situs_numb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'situs_st_1': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'situs_stat': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'situs_stre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'situs_type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lots']