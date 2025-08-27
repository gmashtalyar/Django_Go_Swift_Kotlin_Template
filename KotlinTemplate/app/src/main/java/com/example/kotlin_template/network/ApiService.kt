package com.example.kotlin_template.network

import androidx.compose.runtime.snapshots.SnapshotStateList
import com.example.kotlin_template.model.UserModel
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*


interface ApiService {
    @POST("swift/{api_path}")
    @Headers("Content-Type: application/json")
    suspend fun postComment(
        @Path("api_path") api_path: String,
        @Body commentJSON: CommentJSON
    ): Unit

    @POST("swift/{api_path}")
    @Headers("Content-Type: application/json")
    suspend fun postLogin(
        @Path("api_path") api_path: String,
        @Body loginJSON: LoginJSON
    ): UserModel

    @POST("swift/{api_path}")
    @Headers("Content-Type: application/json")
    suspend fun postDeviceToken(
        @Path("api_path") api_path: String,
        @Body deviceJSON: DeviceJSON
    ): Unit

    @POST("swift/{api_path}")
    @Headers("Content-Type: application/json")
    suspend fun postNotiSettings(
        @Path("api_path") api_path: String,
        @Body notiSettingsJSON: NotiSettingsJSON
    ) : Unit

    @GET("swift/{api_path}")
    suspend fun getNotiSettings(
        @Path("api_path") api_path: String,
    ): NotiSettingsJSON

    data class CommentJSON(
        val client_inn: String,
        val author: Int,
        val comment: String,
        val comment_date: String
    )

    data class LoginJSON(
        val username: String,
        val email: String,
        val password: String,
    )

    data class DeviceJSON(
        val registration_id: String,
        val device_type: String,
        val user_id: Int,
        val email: String
    )

    data class NotiSettingsJSON(
        val user_id: Int, val status_notifications: List<String>, val comments_notifications: Int,
        val late_debt_notifications: Int, val resolution_notifications: Int, val email: String, val device_type: String)

    companion object{
        //        var apiService : ApiService? = null
        @Volatile private var apiService: ApiService? = null
        fun getData(server_link: String) : ApiService {
            if (apiService == null) {
                apiService = Retrofit.Builder()
                    .baseUrl(server_link)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build().create(ApiService::class.java)
            }
            return apiService!!
        }
        fun getDataPublicServer(): ApiService {
            return Retrofit.Builder()
                .baseUrl("https://www.XXXXXX.ru/") // Hardcoded base URL
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(ApiService::class.java)
        }
    }
}

