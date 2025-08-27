package com.example.kotlin_template.viewModel

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.kotlin_template.network.ApiService
import kotlinx.coroutines.launch

class CommentsViewModel: ViewModel() {

    var errorMessage: String by mutableStateOf("")

    fun postClient(api_path: String, commentJSON: ApiService.CommentJSON, server_link: String) {
        viewModelScope.launch {
            val apiService = ApiService.getData(server_link=server_link)
            try {
                Log.d("COMMENT_VIEWMODEL", "Sending POST request with commentJSON: $commentJSON")
                val response = apiService.postComment(api_path, commentJSON)
                Log.d("COMMENT_VIEWMODEL", "Response: $response")
            } catch (e: Exception) {
                errorMessage = e.message.toString()
                Log.d("COMMENT_VIEWMODEL", "Error $errorMessage")
            }
        }
    }
}