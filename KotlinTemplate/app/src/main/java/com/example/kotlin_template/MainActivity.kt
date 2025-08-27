package com.example.kotlin_template

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.compose.rememberNavController
import com.example.kotlin_template.ui.theme.KotlinTemplateTheme
import com.example.kotlin_template.viewModel.*
import kotlin.getValue

class MainActivity : ComponentActivity() {

    val commentsViewModel by viewModels<CommentsViewModel>()
    val userViewModel by viewModels<UserViewModel>()
    val notificationSettingsViewModel by viewModels<NotificationSettingsViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val navController = rememberNavController()

            KotlinTemplateTheme {

                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    NavigationGraph( commentsViewModel=commentsViewModel, userViewModel=userViewModel,
                        notificationSettingsViewModel=notificationSettingsViewModel)
                }
            }
        }
    }
}


