#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
_db.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''
import _env
from _kit import Query, escape
from config import DB_CONFIG
import connection
connection.THREAD_SAFE = False
import sqlstore
from util import lower_name

SQLSTORE = sqlstore.SqlStore(db_config=DB_CONFIG, charset='utf8')
def db_by_table(table):
    return SQLSTORE.get_db_by_table(table)

def cursor_by_table(table):
    return db_by_table(table).cursor()






class ModelCache(object):
    models = {}

    def add(self, model):
        self.models[model.__name__] = model

    def get(self, model_name):
        return self.models[model_name]

cache = ModelCache()

class ModelBase(type):
    '''
    Metaclass for Model

    Sets up default table name and primary key
    Adds fields from table as attributes
    Creates ValidatorChains as necessary

    '''
    def __new__(cls, name, bases, attrs):
        #print "init",name
        if name == 'Model' :
            return super(ModelBase, cls).__new__(cls, name, bases, attrs)

        new_class = type.__new__(cls, name, bases, attrs)

        if not getattr(new_class, 'Meta', None):
            class Empty:
                pass
            new_class.Meta = Empty

        if not getattr(new_class.Meta, 'table', None):
            new_class.Meta.table = lower_name(name)
        new_class.Meta.table_safe = escape(new_class.Meta.table)

        # Assume id is the default
        #if not getattr(new_class.Meta, 'pk', None):
        new_class.Meta.pk = 'id'
        # if not getattr(new_class.Meta, 'mc_key', None):
        #     mc_ver = getattr(new_class.Meta, "mc_ver", "")
        #     if mc_ver:
        #         new_class.Meta.mc_key = "%s@%s:%%s"%(name, mc_ver)
        #     else:
        new_class.Meta.mc_key = '%%s$%s'%name

        db = new_class.db = db_by_table(new_class.Meta.table)

        q = db.cursor()
        q.execute('SELECT * FROM %s LIMIT 0' % new_class.Meta.table_safe)
        q.connection.commit()

        new_class._fields = [f[0] for f in q.description]

        cache.add(new_class)
        return new_class

class Model(object):
    '''
    Allows for automatic attributes based on table columns.

    Syntax::

        from zsql.model import Model
        class MyModel(Model):
            class Meta:
                # If field is blank, this sets a default value on save
                class default:
                    field = 1

                # Table name is lower-case model name by default
                # Or we can set the table name
                table = 'mytable'

        # Create new instance using args based on the order of columns
        m = MyModel(1, 'A string')

        # Or using kwargs
        m = MyModel(col=1, text='A string')

        # Saving inserts into the database (assuming it validates [see below])
        m.save()

        # Updating attributes
        m.field = 123

        # Updates database record
        m.save()

        # Deleting removes from the database
        m.delete()

        m = MyModel(col=0)

        m.save()

        # Retrieval is simple using Model.get
        # Returns a Query object that can be sliced
        MyModel.get(id)

        # Returns a MyModel object with an id of 7
        m = MyModel.get(7)

        # Limits the query results using SQL's LIMIT clause
        # Returns a list of MyModel objects
        m = MyModel.where()[:5]   # LIMIT 0, 5
        m = MyModel.where()[10:15] # LIMIT 10, 5

        # We can get all objects by slicing, using list, or iterating
        m = MyModel.get()[:]
        m = list(MyModel.where(name="zsp").where("age<%s",18))
        for m in MyModel.where():
            # do something here...

        # We can where our Query
        m = MyModel.where(col=1)
        m = m.where(another_col=2)

        # This is the same as
        m = MyModel.where(col=1, another_col=2)

        # Set the order by clause
        m = MyModel.where(col=1).order_by('-field')
        # Removing the second argument defaults the order to ASC

    '''
    __metaclass__ = ModelBase
    
    def __eq__(self, other):
        if other is not None:
            sid = self.id
            oid = other.id
            if sid is not None and oid is not None:
                return sid == oid
        return False
    
    @classmethod
    def max_id(cls):
        c = cls.raw_sql('select max(id) from %s'%cls.Meta.table)
        id = c.fetchone()
        if id:
            return id[0]
        return 0
    
    def __ne__(self, other):
        return not (self == other)

    def __init__(self, *args, **kwargs):
        'Allows setting of fields using kwargs'
        self.__dict__[self.Meta.pk] = None
        self._new_record = True
        for i, arg in enumerate(args):
            self.__dict__[self._fields[i]] = arg
        for i in self._fields[len(args):]:
            self.__dict__[i] = kwargs.get(i)
        self.__dict__['_changed'] = set()

    def __setattr__(self, name, value):
        'Records when fields have changed'
        dc = self.__dict__
        if name[0] != '_':
            fields = self._fields
            if name in fields:
                dc_value = dc[name]
                if dc_value is None:
                    self._changed.add(name)
                else:
                    if value is not None:
                        value = type(dc_value)(value)
                    if dc_value != value:
                        self._changed.add(name)
        dc[name] = value


    def _get_pk(self):
        'Sets the current value of the primary key'
        return getattr(self, self.Meta.pk, None)

    def _set_pk(self, value):
        'Sets the primary key'
        return setattr(self, self.Meta.pk, value)

    def _update(self):
        if not self._changed:return
        'Uses SQL UPDATE to update record'
        query = 'UPDATE %s SET ' % self.Meta.table_safe
        query += ','.join(['%s=%%s' % escape(f) for f in self._changed])
        query += ' WHERE %s=%%s ' % (escape(self.Meta.pk))

        values = [getattr(self, f) for f in self._changed]
        values.append(self._get_pk())

        cursor = Query.raw_sql(query, values, self.db)

    def save(self):
        if self._new_record:
            self._set_default()
            self._new_save()
            self._new_record = False
        else:
            self._update()
        self._changed.clear()
        return self

    def _new_save(self):
        'Uses SQL INSERT to create new record'
        # if pk field is set, we want to insert it too
        # if pk field is None, we want to auto-create it from lastrowid
        pk = self._get_pk()
        auto_pk = 1 and (pk is None) or 0
        fields = [
            f for f in self._fields
            if f != self.Meta.pk or not auto_pk
        ]

        used_fields = []
        values = []
        for i in fields:
            v = getattr(self, i, None)
            #print i,v
            if v is not None:
                used_fields.append(escape(i))
                values.append(v)
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (self.Meta.table_safe,
                ', '.join(used_fields),
                ', '.join(['%s'] * len(used_fields))
        )
        cursor = Query.raw_sql(query, values, self.db)



        if pk is None:
            self._set_pk(cursor.lastrowid)
        return True

    def _set_default(self):
        if hasattr(self.Meta, 'default'):
            default = self.Meta.default
            i = default()

            for k, v in default.__dict__.iteritems():
                if k[0] != '_' :
                    if getattr(self, k, None) is None:
                        if callable(v):
                            v = getattr(i, k)()
                        setattr(self, k, v)
    @classmethod
    def raw_sql(cls, query, *args):
        result = Query.raw_sql(query, args, cls.db)
        return result

    def delete(self):
        'Deletes record from database'
        query = 'DELETE FROM %s WHERE `%s` = %%s' % (self.Meta.table_safe, self.Meta.pk)
        values = [getattr(self, self.Meta.pk)]
        Query.raw_sql(query, values, self.db)

    def update(self, **kwds):
        set_what = ','.join(
            '%s=%%s'%(
                escape(k)
            )
            for k in kwds.keys()
        )
        query = 'UPDATE %s SET %s WHERE `%s` = %%s' % (
            self.Meta.table_safe,
            set_what, self.Meta.pk
        )
        values = kwds.values()+[getattr(self, self.Meta.pk)]
        Query.raw_sql(query, values, self.db)


    @classmethod
    def where(cls, *args, **kwargs):
        'Returns Query object'
        return Query(
            model=cls,
            args=args,
            conditions=kwargs
        )


    @classmethod
    def count(cls, *args, **kwargs):
        return Query(
            model=cls,
            args=args,
            conditions=kwargs
        ).count(1)


    @classmethod
    def begin(cls):
        """
        begin() and commit() let you explicitly specify an SQL transaction.
        Be sure to call commit() after you call begin().
        """
        db = cls.db
        db.b_commit = False

    @classmethod
    def commit(cls):
        db = cls.db
        try:
            cursor = db.cursor()
            cursor.connection.commit()
        finally:
            db.b_commit = True

    @classmethod
    def rollback(cls, db=None):
        db = cls.db
        try:
            cursor = db.cursor()
            cursor.connection.rollback()
        finally:
            db.b_commit = True

    @classmethod
    def get(cls, __obj_pk=None, **kwargs):
        if __obj_pk is None:
            if not kwargs:
                return
        else:
            kwargs = {
                'id': __obj_pk
            }
        q = Query(model=cls, conditions=kwargs)
        q.limit = (0, 1)
        q = q.execute_query()
        q = q.fetchone()
        if q:
            obj = cls(*q)
            obj.__dict__['_new_record'] = False
            return obj
    
    @classmethod
    def get_or_create(cls, **kwds):
        ins = cls.get(**kwds)
        if ins is None:
            ins = cls(**kwds)
        return ins

    @classmethod
    def replace_into(cls, **kwds):
        pk = cls.Meta.pk
        if pk in kwds:
            id = kwds[pk]
            ins = cls.get(id)
            if ins is None:
                ins = cls(id=id)
            del kwds[pk]
        else:
            ins = cls()

        for k, v in kwds.iteritems():
            setattr(ins, k, v)
        ins.save()

        return ins

    @classmethod
    def get_list(cls, id_list):
        res = []
        id_list = tuple(id_list)
        return cls.where('id in (%s)'%(','.join([str(i) for i in id_list])))
