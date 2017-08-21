# _*_ coding:utf-8_*_

class BaseDB(object):

    def __init__(self, conn_read, conn_write, tracker=None):
        self._conn_read = conn_read
        self._conn_write = conn_write
        self._tracker = tracker
        # print self._conn_read
        # print self._conn_write


    def start_transaction(self):
        '''
                        开启事务
        '''
        self._conn_write.execute('BEGIN')


    def commit(self):
        '''
                        提交事务
        '''
        self._conn_write.execute('COMMIT')


    def rollback(self):
        '''
                        回滚事务
        '''
        self._conn_write.execute('ROLLBACK')


    def update(self, table_name, data={}, condition_data=None, incr_data=None):
        '''
        根据条件更新

        Args:
            table_name: 更新的表名
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
            data: 参数字典,例如{'name':'zhangsan','age':12}
            upsert: 布尔型,True:则进行save_or_update操作.False:进行update操作
        Returns:
        '''

        items = ['UPDATE %s SET ' % (table_name)]
        if data:
            for key in data:
                value = data.get(key)
                if isinstance(value, (int, long, float)) or 'now()' == value:
                    items.append("%s=%s,"% (key, value))
                else:
                    items.append('%s="%s",'% (key, value))

        if incr_data:
            for key in incr_data:
                value = incr_data.get(key)
                items.append('%s=%s+%s,' % (key, key, value))
        sql = ''.join(items)

        condition_str = ''
        if condition_data:
            condition_list = [" WHERE 1=1"]
            for key in condition_data:
                value = condition_data.get(key)
                if isinstance(value, (int, long, float)):
                    condition_list.append(' AND ' + key + '=%s' % (value))
                elif isinstance(value, tuple):
                    dst_str = str(value)
                    condition_list.append(' AND ' + key + 'in %s' % (dst_str))
                else:
                    condition_list.append(' AND ' + key + '="%s"' % (value))
        condition_str = ''.join(condition_list)
        sql = sql[0:len(sql)-1] + condition_str
        # print sql
        return self._conn_write.execute_rowcount(sql)


    def select(self, table_name, fields=None, condition_data=None, orderby=None, limit=None, is_transaction=False):
        '''
        单表查询通用方法,支持指定查询字段,查询条件,模糊查询,排序查询

        Args:
            table_name: 查询的表名,字符串类型
            fields: 需要查询的字段,list类型,例如['name','age']
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
            fuzzy: condition_data中要模糊查询的键,list类型,例如需要 name like '%张%'时使用  ['name']
            orderby: 排序条件,列表,例如[('age', 'DESC'), ('id', 'ASC')]
            limit: 分页查询,元组,例如(0,1)
        Returns:
            result: list类型,其中的元素是字典类型
        '''

        items = ['SELECT ']
        if not fields:
            items.append('*')
        else:
            for field in fields:
                items.append(field+',')
        sql_str = ''.join(items)
        sql_str = sql_str[0:len(sql_str)-1] + " FROM " + table_name
        condition_str = ''
        if condition_data:
            condition_list = [' WHERE 1=1']
            for key in condition_data:
                value = condition_data.get(key)
                if isinstance(value, (int, float)):
                    condition_list.append(' AND ' + key + '=%s' % (value))
                elif isinstance(value, tuple):
                    dst_str = str(tuple)
                    condition_list.append(' AND ' + key + 'in %s' % (dst_str))
                else:
                    condition_list.append(' AND ' + key + '="%s"' % (value))
            condition_str = ''.join(condition_list)

        orderby_str = ''
        if orderby:
            orderby_list = []
            for item in orderby:
                orderby_list.append(item[0] + " " + item[1])
            orderby_str = " ORDER BY " + ','.join(orderby_list)

        limit_str = ''
        if isinstance(limit, int):
            limit_str = ' LIMIT %s' % limit
        elif limit:
            if len(limit) == 1:
                limit_str = ' LIMIT %s' % limit
            elif len(limit) == 2:
                limit_str = ' LIMIT %s,%s' % limit

        sql = sql_str + condition_str + orderby_str + limit_str
        # print sql
        if is_transaction:
            result = self._conn_write.query(sql)
        else:
            result = self._conn_read.query(sql)
        return result

    def insert(self, table_name, data):
        items = ["INSERT IGNORE INTO %s(" % table_name]
        values = ["VALUE("]

        for key in data:
            items.append('%s,' % key)
            value = data.get(key)
            if isinstance(value, (int,float,long)):
                values.append('%s,' % value)
            else:
                values.append('"%s",' % value)
        items_str = ''.join(items)
        items_str = items_str[0:len(items_str)-1] + ')'
        values_str = ''.join(values)
        values_str = values_str[0:len(values_str)-1] + ')'

        sql = items_str + values_str
        return self._conn_write.execute_lastrowid(sql)

    def delete(self, table_name, condition_data=None):
        '''
        根据条件删除

        Args:
            table_name: 更新的表名
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
        Returns:
        '''

        assert condition_data, "Are you serious? The whole table will be delete!!!"

        sql = "delete from %s"% (table_name)

        # 拼' WHERE 1=1 AND xxx=xxx AND xxx like "%xx"'部分
        condition_list = [" WHERE 1=1"]
        for key in condition_data:
            value = condition_data.get(key)
            if isinstance(value, (int,long,float)):
                condition_list.append(" AND "+key+"=%s"% (value))
            elif isinstance(value, tuple):
                dst_str = str(value)
                condition_list.append(" AND "+key+" in %s"% (dst_str))
            else:
                condition_list.append(" AND "+key+"='%s'"% (value))

        condition_str = ''.join(condition_list)
        sql += condition_str

        return self._conn_write.execute_rowcount(sql)
