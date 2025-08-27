package com.example.kotlin_template.viewModel

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class UserDataStore(private val context: Context) {

    companion object {
        private val Context.dataStore: DataStore<Preferences> by preferencesDataStore("UserData")
        val USER_ID = intPreferencesKey("user_id")
        val USER_EMAIL = stringPreferencesKey("user_email")
        val USER_FIRST_NAME = stringPreferencesKey("user_first_name")
        val USER_LAST_NAME = stringPreferencesKey("user_last_name")
        val USER_USERNAME = stringPreferencesKey("user_username")
        val USER_API_URL = stringPreferencesKey("user_api_url")
        val USER_OTDEL = stringPreferencesKey("user_otdel")
        val USER_DIRECTOR_ID = intPreferencesKey("user_director_id")
        val USER_DEPARTMENT = stringPreferencesKey("user_department")
        val USER_USER_GROUP = stringPreferencesKey("user_user_group")
    }


    val getUserData: Flow<UserDataStoreClass> = context.dataStore.data
        .map { preferences ->
            UserDataStoreClass(
                preferences[USER_ID] ?: 0,
                preferences[USER_EMAIL] ?: "",
                preferences[USER_FIRST_NAME] ?: "",
                preferences[USER_LAST_NAME] ?: "",
                preferences[USER_USERNAME] ?: "",
                preferences[USER_API_URL] ?: "",
                preferences[USER_OTDEL] ?: "",
                preferences[USER_DIRECTOR_ID] ?: 0,
                preferences[USER_DEPARTMENT] ?: "",
                preferences[USER_USER_GROUP] ?: ""
            )
        }

    data class UserDataStoreClass(
        val id: Int,
        val email: String,
        val firstName: String,
        val lastName: String,
        val username: String,
        val apiUrl: String,
        val otdel: String,
        val directorId: Int,
        val department: String,
        val userGroup: String
    )


    suspend fun saveUserData(id: Int, email: String, first_name: String, last_name: String, username: String,
                             api_url: String, otdel: String, director_id: Int, department: String, user_group: String) {
        context.dataStore.edit { preferences ->
            preferences[USER_ID] = id
            preferences[USER_EMAIL] = email
            preferences[USER_FIRST_NAME] = first_name
            preferences[USER_LAST_NAME] = last_name
            preferences[USER_USERNAME] = username
            preferences[USER_API_URL] = api_url
            preferences[USER_OTDEL] = otdel
            preferences[USER_DIRECTOR_ID] = director_id
            preferences[USER_DEPARTMENT] = department
            preferences[USER_USER_GROUP] = user_group
        }
    }
}
