package com.example.kotlin_template.viewModel

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.kotlin_template.model.UserModel
import com.example.kotlin_template.network.ApiService
import com.google.android.gms.common.api.ApiException
import kotlinx.coroutines.launch

sealed class LoginError {
    object InvalidCredentials : LoginError()
    object NetworkError : LoginError()
    object UnknownError : LoginError()
}

class UserViewModel: ViewModel() {

    sealed class LoginResult {
        data class Success(val user: UserModel): LoginResult()
        data class Failure(val error: LoginError): LoginResult()
        object Initial : LoginResult()
    }

    var login_result: LoginResult by mutableStateOf(LoginResult.Initial)

    var user_response: UserModel by mutableStateOf(UserModel(
        id = 0, email = "", first_name = "", last_name = "", username = "", api_url = "", otdel = "", director_id = 0,
        department = "", user_group = ""))
    var errorMessage: String by mutableStateOf("")

    fun login_user(api_path: String, loginJSON: ApiService.LoginJSON) {
        viewModelScope.launch {
            val apiService = ApiService.getData(server_link="https://www.credit-app.ru/")
            try {
                Log.d("USER_VIEWMODEL", "Logging user ...")
                val user = apiService.postLogin(api_path=api_path, loginJSON=loginJSON)
                user_response = user
                login_result = LoginResult.Success(user)
            } catch(e: Exception) {
                errorMessage = e.message.toString()
                Log.d("USER_VIEWMODEL", "Error $errorMessage")
                login_result = LoginResult.Failure(mapError(e))
            }
        }
    }

    private fun mapError(e: Exception): LoginError {
        return when (e) {
            is java.net.UnknownHostException -> LoginError.NetworkError
            is java.net.SocketTimeoutException -> LoginError.NetworkError
            is java.io.IOException -> LoginError.NetworkError
            is ApiException -> {
                if (e.message?.contains("401") == true) {
                    LoginError.InvalidCredentials
                } else { LoginError.UnknownError }}
            else -> LoginError.UnknownError
        }
    }

}
