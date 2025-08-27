package com.example.kotlin_template.view

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun LoadingScreen() {
    Text("Загрузка", style= MaterialTheme.typography.titleLarge, fontWeight= FontWeight.Bold)
}


@Preview(showBackground=true)
@Composable
fun LoadingScreenPreview() {
    LoadingScreen()
}