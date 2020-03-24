from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 sql_stmts=""
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_stmts = sql_stmts

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        self.log.info('DataQualityOperator started.')
        for (sql_stmt, answer) in self.sql_stmts:
            row = redshift_hook.get_first(sql_stmt)
            if row is not None:
                if row[0] == answer:
                    self.log.info("Test {} Passed.".format(sql_stmt))
                else:
                    raise ValueError("Test {} Failed.".format(sql_stmt))

        self.log.info('DataQualityOperator finished.')
        