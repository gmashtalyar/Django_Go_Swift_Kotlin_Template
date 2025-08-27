package com.example.kotlin_template

sealed class Screen(val route: String) {
    object Login_Form : Screen("login_form")
    object Settings_Form : Screen("settings_form")
    data class Comment_Screen_Class(val clientId: String, val comment_type: String) : Screen("comment/$clientId/$comment_type")
    data class NonPDFDocument(val non_pdf: String) : Screen("document/$non_pdf")
}

