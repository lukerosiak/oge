CREATE INDEX oge_document_date_idx ON oge_document(date);

ALTER TABLE oge_document ADD COLUMN search_index TSV;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON oge_document FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(search_index, 'pg_catalog.english', header, text);

CREATE INDEX oge_document_search_index_idx ON oge_document USING gin(search_index);

