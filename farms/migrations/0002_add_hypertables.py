from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("farms", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL("SELECT create_hypertable('farms_sensorreading', 'time');"),
        migrations.RunSQL(
            "ALTER TABLE farms_sensorreading SET (timescaledb.compress, timescaledb.compress_segmentby = 'sensor_id');"
        ),
        migrations.RunSQL(
            "SELECT add_compress_chunks_policy('farms_sensorreading', INTERVAL '7 days');"
        ),
    ]
