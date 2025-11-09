package handlers

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"project/helpers" // adjust to your module path

	_ "github.com/lib/pq"
)

// Template DB connection
func GetDBConnection() (*sql.DB, error) {
	connStr := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASSWORD"),
		os.Getenv("DB_NAME"),
	)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("error opening DB: %v", err)
	}
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("error pinging DB: %v", err)
	}
	return db, nil
}

// Handler: GET /api/chart-data
func HandleGetChartData(w http.ResponseWriter, r *http.Request) {
	db, err := GetDBConnection()
	if err != nil {
		log.Printf("DB connection failed: %v", err)
		http.Error(w, "Database connection failed", http.StatusInternalServerError)
		return
	}
	defer db.Close()

	rows, err := db.Query(`SELECT id, name, value FROM template_data ORDER BY id`)
	if err != nil {
		log.Printf("Error querying template_data: %v", err)
		http.Error(w, "Failed to query data", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var results []helpers.TemplateData
	for rows.Next() {
		var row helpers.TemplateData
		if err := rows.Scan(&row.ID, &row.Name, &row.Value); err != nil {
			log.Printf("Error scanning row: %v", err)
			http.Error(w, "Failed to read data", http.StatusInternalServerError)
			return
		}
		results = append(results, row)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status": "ok",
		"data":   results,
	})
}
