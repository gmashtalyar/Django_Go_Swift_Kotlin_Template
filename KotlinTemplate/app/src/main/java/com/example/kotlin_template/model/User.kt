package com.example.kotlin_template.model

import com.google.gson.annotations.SerializedName

data class UserModel (
    @SerializedName("id") val id: Int,
    @SerializedName("email") val email: String,
    @SerializedName("first_name") val first_name: String,
    @SerializedName("last_name") val last_name: String,
    @SerializedName("username") val username: String,
    @SerializedName("api_url") val api_url: String,
    @SerializedName("otdel") val otdel: String,
    @SerializedName("director_id") val director_id: Int,
    @SerializedName("department") val department: String,
    @SerializedName("user_group") val user_group: String,
)

