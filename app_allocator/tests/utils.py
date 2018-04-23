        
def assert_only_these_fields_in_csv_row(fields, csv_row):
    csv_fields = set(csv_row.split(","))
    fields = [str(field) for field in fields]
    csv_fields.discard("")
    assert len(csv_fields) == len(fields)
    for field in fields:
        assert field in csv_fields
    
