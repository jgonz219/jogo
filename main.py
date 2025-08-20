from bigquery import Bigquery
from whoop import Whoop

def main():
    bigquery = Bigquery()
    whoop = Whoop()

    workout_collection_df = whoop.get_workout_collection()
    bigquery.write_truncate_table('raw_whoop', 'raw_workout_collection', workout_collection_df)

    cycle_collection_df = whoop.get_cycle_collection()
    bigquery.write_truncate_table('raw_whoop', 'raw_cycle_collection', cycle_collection_df)
    
    recovery_collection_df = whoop.get_recovery_collection()
    bigquery.write_truncate_table('raw_whoop', 'raw_recovery_collection', recovery_collection_df)

    sleep_collection_df = whoop.get_sleep_collection()
    bigquery.write_truncate_table('raw_whoop', 'raw_sleep_collection', sleep_collection_df)

if __name__ == '__main__':
    main()