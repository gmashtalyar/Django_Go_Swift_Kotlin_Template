package com.example.kotlin_template.viewModel

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.gson.JsonParseException
import com.example.kotlin_template.network.ApiService
import kotlinx.coroutines.launch
import retrofit2.HttpException
import java.io.IOException

class DeviceTokenViewModel: ViewModel() {

    var error_message: String by mutableStateOf("")

    fun sendDeviceToken(api_path: String, deviceJSON: ApiService.DeviceJSON) {
        viewModelScope.launch {
            val apiService = ApiService.getDataPublicServer()
            Log.d("TOKEN_VIEWMODEL", "Sending POST with server_link: https://www.XXXXXXX.ru/")
            try {
                Log.d("TOKEN_VIEWMODEL", "Sending POST with deviceJSON: $deviceJSON")
                val response = apiService.postDeviceToken(api_path, deviceJSON)
                Log.d("TOKEN_VIEWMODEL", "Response: $response")
            } catch (e: JsonParseException) {
                error_message = "Malformed JSON: ${e.message}"
                Log.e("TOKEN_VIEWMODEL", "Malformed JSON: $error_message", e)
            } catch (e: IOException) {
                error_message = "Network error: ${e.message}"
                Log.e("TOKEN_VIEWMODEL", "Network error: $error_message", e)
            } catch (e: HttpException) {
                val errorBody = e.response()?.errorBody()?.string()
                Log.e("TOKEN_VIEWMODEL", "HTTP Exception: ${e.code()}, Message: $errorBody")
            } catch(e:Exception) {
                error_message = e.message.toString()
                Log.e("TOKEN_VIEWMODEL", "Error $error_message ")
                Log.e("TOKEN_VIEWMODEL", "path https://www.XXXXXXX.ru/ swift/$api_path")
                Log.e("TOKEN_VIEWMODEL", "Payload: $deviceJSON")
            }
        }
    }
}

