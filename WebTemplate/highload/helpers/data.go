package helpers

// TemplateData represents a single record from the template_data table.
type TemplateData struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Value int    `json:"value"`
}
