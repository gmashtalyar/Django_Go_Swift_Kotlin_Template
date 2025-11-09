package main

import (
	"log"
	"net/http"
	"os"

	"project/handlers" // adjust module path to your project name
)

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()

	// Example Open API endpoint
	mux.HandleFunc("/api/chart-data", handlers.HandleGetChartData)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server is running on port %s", port)
	err := http.ListenAndServe(":"+port, corsMiddleware(mux))
	if err != nil {
		log.Fatal("Server failed:", err)
	}
}
