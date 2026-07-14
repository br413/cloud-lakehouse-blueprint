resource "aws_glue_catalog_database" "lakehouse" {
  name        = replace("${var.project_name}_${var.environment}", "-", "_")
  description = "Governed metadata catalog for medallion lakehouse layers"
}

resource "aws_glue_catalog_table" "layer_tables" {
  for_each = var.bucket_names

  name          = each.key
  database_name = aws_glue_catalog_database.lakehouse.name

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${each.value}/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
    }
  }

  parameters = {
    classification = "parquet"
    layer          = each.key
  }
}

output "database_name" {
  value = aws_glue_catalog_database.lakehouse.name
}
