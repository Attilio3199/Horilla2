from django.db import migrations


class Migration(migrations.Migration):
    """Restore the inherited audit columns on legacy document tables safely."""

    dependencies = [("horilla_documents", "0002_document_categories_maternity")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE horilla_documents_documentcategory
                    ADD COLUMN IF NOT EXISTS created_at timestamptz NULL,
                    ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT true,
                    ADD COLUMN IF NOT EXISTS created_by_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS modified_by_id bigint NULL;
                ALTER TABLE horilla_documents_documentsubcategory
                    ADD COLUMN IF NOT EXISTS created_at timestamptz NULL,
                    ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT true,
                    ADD COLUMN IF NOT EXISTS created_by_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS modified_by_id bigint NULL;
                ALTER TABLE horilla_documents_maternita
                    ADD COLUMN IF NOT EXISTS created_at timestamptz NULL,
                    ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT true,
                    ADD COLUMN IF NOT EXISTS created_by_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS modified_by_id bigint NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
