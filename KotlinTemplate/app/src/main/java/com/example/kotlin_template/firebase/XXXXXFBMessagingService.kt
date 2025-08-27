package com.example.kotlin_template.firebase

import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.example.kotlin_template.MainActivity
import com.example.kotlin_template.dataStoreFB
import com.example.kotlin_template.R
import com.example.kotlin_template.network.ApiService
import com.example.kotlin_template.viewModel.DeviceTokenViewModel
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.google.firebase.messaging.remoteMessage


class XXXXXFBMessagingService: FirebaseMessagingService() {

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        val title = message.notification?.title ?: "Default title"
        val body = message.notification?.title ?: "Default body"
        val clientID = message.data["clientID"]?.toIntOrNull()

        Log.v("Cloud Message", "From ${message.from}")

        clientID?.let {
            val intent = Intent(this, MainActivity::class.java)
            intent.putExtra("clientID", it)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        if(message.data.isNotEmpty()){
            Log.v("Cloud Message", "Message data ${message.data}")
        }

        message.data.let {
            Log.v("Cloud Message", "Message notification body ${it["body"]}")
        }

        if (message.notification != null) {
            Log.v("Cloud Message", "Notification  ${message.notification}")
            Log.v("Cloud Message", "Notification Title ${message.notification!!.title}")
            Log.v("Cloud Message", "Notification Body ${message.notification!!.body}")

            createNotification(title, body)

        }
    }

    private fun createNotification(title: String, body: String) {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        val notificationBuilder = NotificationCompat.Builder(this, "default")
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.logo_notification)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true) // why?

        notificationManager.notify(1, notificationBuilder.build())
    }


    override fun onNewToken(token: String) {
        super .onNewToken(token)
        GlobalScope.launch {
            saveGCMToken(token)
            sendTokenToServer(token)
        }
    }

    private suspend fun saveGCMToken(token: String) {
        val gckTokenKey = stringPreferencesKey("FMC_token")
        baseContext.dataStoreFB.edit { pref ->
            pref[gckTokenKey] = token
        }
    }


    private suspend fun sendTokenToServer(token: String) {
        try {
            val deviceTokenViewModel = DeviceTokenViewModel()
            val deviceJSON = ApiService.DeviceJSON(registration_id = token, device_type = "Android",
                user_id = 0, email = "")
            deviceTokenViewModel.sendDeviceToken(api_path = "register_device/", deviceJSON = deviceJSON)
            Log.d("Cloud Message", "Token sent to server successfully")
        } catch (e: Exception) {
            Log.e("Cloud Message", "Error sending token to server: ${e.message}")
        }
    }
}

