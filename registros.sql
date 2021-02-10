CREATE TABLE IF NOT EXISTS registros (
  id INTEGER PRIMARY KEY,                                      
  record_date         DATE NOT NULL,
  record_time         TEXT NOT NULL,
  lectura             INTEGER NOT NULL
)