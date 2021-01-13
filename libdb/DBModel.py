from .config import db_url, schema, allowed_loas
from sqlalchemy import create_engine, text, select, Table, MetaData
from .ViEWSModel import ModelLOA, ModelTV
from typing import List


class Run:
    def __init__(self, id, engine, schema=schema):
        self.engine = engine
        self.schema = schema
        self.id = id.lower()
        self.model_tree = None

    def __model_leaf(self, parent='', loa='cm', tv='sb'):
        query = text(f"""
SELECT node FROM structure.model
WHERE
generation_id IN (SELECT DISTINCT generation_id FROM structure.register WHERE run ilike :id AND loa=:loa)
AND parent = :parent AND loa ilike :loa AND type_of_violence ilike :tv
""")
        with self.engine.connect() as conn:
            models = conn.execute(query, id=self.id, parent=parent, loa=loa, tv=tv).fetchall()
            if not models:
                return [(parent, None)]
            else:
                return [(parent, i[0]) for i in models]

    def __model_iterate(self, parent='', loa='cm', tv='sb'):
        temp_data = self.__model_leaf(parent, loa, tv)
        for i in temp_data:
            if i[1] is None:
                return []
            else:
                return temp_data + self.__model_iterate(parent=i[1], loa=loa, tv=tv)

    def __sugar_dict(self, model_component):
        return [{'parent': i, 'node': j} for (i, j) in model_component]

    def __fetch_model_tree(self):
        self.model_tree = ModelLOA(cm=ModelTV(sb=self.__sugar_dict(self.__model_iterate(loa='cm', tv='sb')),
                                              ns=self.__sugar_dict(self.__model_iterate(loa='cm', tv='ns')),
                                              os=self.__sugar_dict(self.__model_iterate(loa='cm', tv='os'))),
                                   pgm=ModelTV(sb=self.__sugar_dict(self.__model_iterate(loa='pgm', tv='sb')),
                                               ns=self.__sugar_dict(self.__model_iterate(loa='pgm', tv='ns')),
                                               os=self.__sugar_dict(self.__model_iterate(loa='pgm', tv='os'))
                                               ))

    def fetch_model_tree(self):
        if self.model_tree is None:
            self.__fetch_model_tree()
        return self.model_tree


class Runs:
    def __init__(self, url=db_url):
        self.url = url
        self.engine = create_engine(url)
        self.runs = self.__fetch_runs()

    def __fetch_runs(self):
        conn = self.engine.connect()
        query = text(f"SELECT DISTINCT LOWER(run) FROM structure.register ORDER BY LOWER(run) ASC")
        av_runs = conn.execute(query).fetchall()
        av_runs = {i[0]: Run(i[0], self.engine) for i in av_runs}
        return av_runs

    def list_runs(self):
        return (list(self.runs.keys()))

    def is_run(self, run_id):
        return run_id.lower() in self.runs.keys()

    def get_run(self, run_id):
        if not self.is_run(run_id):
            raise KeyError("No such model exists!")
        else:
            return self.runs[run_id.lower()]

    def dirty_full_model_list(self):
        conn = self.engine.connect()
        query = text(f"SELECT DISTINCT node FROM structure.model")
        dirty_list = conn.execute(query).fetchall()
        dirty_list = [i[0] for i in dirty_list]
        conn.close()
        return dirty_list


class PageFetcher:
    def __init__(self, run: object, loa: object, model_list: object, page_size: object = 1000, components: object = False) -> None:
        self.model_list = model_list

        self.limit = page_size

        self.run_id = run.id
        self.engine = run.engine
        self.schema = run.schema
        self.where_queries = []

        self.components = components

        if loa == 'pgm':
            self.table_id = self.run_id + '_pgm'
            self.row_id = 'pg_id'
            self.sugar = []
        else:
            self.table_id = self.run_id + '_cm'
            self.row_id = 'country_id'
            self.sugar = ['name','gwcode','isoab','year','month']

        self.time_id = 'month_id'
        self.data_table = Table(self.table_id, MetaData(), schema=self.schema, autoload_with=self.engine)
        self.row_count, self.page_count = self.__base_counts()

    def __compute_offset(self, page):
        if page < 1:
            page = 1
        offset = (page - 1)*self.limit
        return offset

    def __base_counts(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT row_count FROM structure.register WHERE table_name = :tn")
            row_count = conn.execute(query, run=self.run_id, tn=self.table_id).fetchone()[0]
            page_count = int(row_count / self.limit) + 1
            return row_count, page_count

    def total_counts(self):

        # To avoid wasting a select(count) for no reason.
        # Count queries tend to be slow with large datasets:
        # Main reason is that even w/ indexes a sequential scan
        # Thus:
        # We store the length of the base table on transfer, and look it up at init
        # And only compute a select(count) when we have a filtering element attached.

        if len(self.where_queries) > 0:
            count_query = select(
                [
                    text('count(*)')
                ]
            ).select_from(self.data_table)
            for where_query in self.where_queries:
                count_query = count_query.where(where_query)
            with self.engine.connect() as conn:
                result_set = conn.execute(count_query)
                self.row_count = result_set.fetchone()[0]
                self.page_count = int(self.row_count / self.limit) + 1

        return self.row_count, self.page_count

    def __is_dynasim(self, i):
        query = text("SELECT dynasim::BOOLEAN FROM structure.model WHERE node=:i")
        with self.engine.connect() as conn:
            return conn.execute(query, i=i).fetchone()[0]

    def __frederick_labels(self):
        columns = []
        columns += ['sc_' + i for i in self.model_list if not self.__is_dynasim(i)]
        columns += [i for i in self.model_list if self.__is_dynasim(i)]
        return columns

    @staticmethod
    def __sugar_precision(*args, precision="NUMERIC(10,4)"):
        columns = []
        for col_set in args:
            columns += [i + '::' + precision for i in col_set]
        return list(set(columns))

    def __make_base_columns(self):
        columns = self.__frederick_labels()
        base_columns = [self.row_id, self.time_id] + self.sugar + self.__sugar_precision(columns)
        #print (base_columns)
        return base_columns

    def __make_augmented_columns(self):
        columns = self.__frederick_labels()
        component_columns = []

        with self.engine.connect() as conn:
            for model in columns:
                print(model)
                query = text("SELECT target FROM structure.components WHERE table_name = :tn AND lead = :model ORDER BY target")
                component_set = conn.execute(query, tn=self.table_id, model=model).fetchall()
                component_columns += [i[0] for i in component_set]
        augmented_columns = [self.row_id, self.time_id] + self.sugar + self.__sugar_precision(columns, component_columns)
        return augmented_columns

    def register_where_priogrid(self, priogrid: List):
        if self.row_id == 'pg_id' and priogrid is not None:
            print('priogrid:',priogrid)
            self.where_queries += [text('pg_id = ANY(:pg_id)').bindparams(pg_id=priogrid)]
        if self.row_id == 'country_id' and priogrid is not None:
            print('priogrid->country',priogrid)
            self.where_queries += [text
                                   ('country_id IN (SELECT DISTINCT country_id FROM '
                                    'structure.pg2c WHERE pg_id = ANY(:pg_id))').bindparams(pg_id=priogrid)]

    def register_where_countryid(self, countryid: List):
        if self.row_id == 'pg_id' and countryid is not None:
            self.where_queries += [text
                                   ('pg_id IN (SELECT DISTINCT pg_id FROM '
                                    'structure.pg2c WHERE country_id = ANY(:id))').bindparams(id=countryid)]
        if self.row_id == 'country_id' and countryid is not None:
            self.where_queries += [text('country_id = ANY(:country_id)').bindparams(country_id=countryid)]


    def register_where_monthid(self, monthid: List):
        if monthid is not None:
            print('monthid:', monthid)
            self.where_queries += [text('month_id = ANY(:month_id)').bindparams(month_id=monthid)]


    def fetch(self, page):
        if not self.components:
            augmented_list = self.__make_base_columns()
        else:
            augmented_list = self.__make_augmented_columns()

        offset = self.__compute_offset(page)

        query = select(
            [
                text(', '.join(augmented_list))
            ]
        ).select_from(self.data_table)
        query = query.limit(self.limit)
        query = query.offset(offset)

        if len(self.where_queries)>0:
            for where_query in self.where_queries:
                query = query.where(where_query)

        with self.engine.connect() as conn:
            result_set = conn.execute(query)
            return result_set.fetchall()