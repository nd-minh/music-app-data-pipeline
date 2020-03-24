from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 aws_conn_id="aws_credentials",
                 file_location="",
                 table="",
                 json_path="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.file_location = file_location
        self.table = table
        self.json_path = json_path
        

    def execute(self, context):
        self.log.info('StageToRedshiftOperator started.')
        aws_hook = AwsHook(self.aws_conn_id)     
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(self.redshift_conn_id)
        if self.json_path == "":
            sql_stmt = ("""
                COPY {}
                from {}    
                ACCESS_KEY_ID '{}'
                SECRET_ACCESS_KEY '{}'
                format as json 'auto'
                region 'us-west-2'   
            """).format(self.table,self.file_location,credentials.access_key,credentials.access_key)
            redshift_hook.run(sql_stmt)
        else:
            sql_stmt = ("""
                COPY {}
                from {}    
                ACCESS_KEY_ID '{}'
                SECRET_ACCESS_KEY '{}'
                json '{}'
                region 'us-west-2'   
            """).format(self.table,self.file_location,credentials.access_key,credentials.access_key,self.json_path)
            redshift_hook.run(sql_stmt)

        self.log.info('StageToRedshiftOperator finished.')


