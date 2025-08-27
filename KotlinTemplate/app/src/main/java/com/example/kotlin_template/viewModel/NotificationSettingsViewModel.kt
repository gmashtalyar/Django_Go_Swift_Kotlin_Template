package com.example.kotlin_template.viewModel

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.kotlin_template.network.ApiService
import kotlinx.coroutines.launch

class NotificationSettingsViewModel: ViewModel() {

    var noti_settings: ApiService.NotiSettingsJSON by mutableStateOf(ApiService.NotiSettingsJSON(user_id= 0, status_notifications = emptyList(), comments_notifications= 0, late_debt_notifications= 0, resolution_notifications= 0, email="", device_type="android"))
    var statuses = mutableStateListOf<String>()
    var selected_statuses = mutableStateListOf<String>()
    var error_message: String by mutableStateOf("")



    fun postNotiSettings(api_path: String, notiSettingsJSON: ApiService.NotiSettingsJSON) {
        viewModelScope.launch {
            val apiService = ApiService.getDataPublicServer()
            try{
                Log.d("NOTI_SETTINGS_VM", "Sending POST with notiSettingsJSON: $notiSettingsJSON")
                val response = apiService.postNotiSettings(api_path, notiSettingsJSON)
            } catch (e: Exception) {
                error_message= e.message.toString()
                Log.d("NOTI_SETTINGS_VM", "Error $error_message")
            }
        }
    }

    fun getNotiSettings(api_path: String) {
        viewModelScope.launch {
            val apiService = ApiService.getDataPublicServer()
            try {
                Log.d("NOTI_SETTINGS_VM", "Fetching notiSettingsJSON at $api_path")
                val response = apiService.getNotiSettings(api_path)
                noti_settings = response
                //selected_statuses = response.status_notifications as SnapshotStateList<String>
                selected_statuses.clear()
                selected_statuses.addAll(response.status_notifications)

                Log.d("NOTI_SETTINGS_VM", "selected_statuses fetched as $selected_statuses")
                error_message = ""
            } catch(e:Exception) {
                error_message = e.message.toString()
                Log.d("NOTI_SETTINGS_VM", "Error $error_message")
            }
        }
    }

    fun updateStatusNotifications(label: String, isChecked: Boolean) {
        val updatedStatuses = if (isChecked) {
            //noti_settings.status_notifications + label
            selected_statuses.add(label)
        } else {
            //noti_settings.status_notifications - label
            selected_statuses.remove(label)
        }
        noti_settings = noti_settings.copy(status_notifications = selected_statuses)
        //noti_settings = noti_settings.copy(status_notifications = updatedStatuses, device_type = noti_settings.device_type)
    }

    fun updateCommentNotifications(comments: Boolean, lateDebt: Boolean, resolution: Boolean) {
        noti_settings = noti_settings.copy(
            comments_notifications = if (comments) 1 else 0,
            late_debt_notifications = if (lateDebt) 1 else 0,
            resolution_notifications = if (resolution) 1 else 0
        )
    }
}

