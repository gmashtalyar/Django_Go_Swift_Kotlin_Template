package com.example.kotlin_template.viewModel

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class PasscodePrefStore(private val context: Context) {
    companion object {
        private val Context.dataStore: DataStore<Preferences> by preferencesDataStore("noPIN")
        val preference = booleanPreferencesKey("noPIN")
    }

    val getPasscodePref: Flow<Boolean> = context.dataStore.data.map { preferences -> preferences[preference] ?: false }

    suspend fun truePasscodePref() { context.dataStore.edit { preferences -> preferences[preference] = true } }

    suspend fun falsePasscodePref() { context.dataStore.edit { preferences -> preferences[preference] = false } }
}


class PasscodeDataStore(private val context: Context) {

    companion object {
        private val Context.dataStore: DataStore<Preferences> by preferencesDataStore("passcode")
        val PASSCODE = stringPreferencesKey("passcode")
    }

    val getPasscode: Flow<String?> = context.dataStore.data.map { preferences -> preferences[PASSCODE] ?: "" }

    suspend fun savePasscodeData(passcode: String) { context.dataStore.edit { preferences -> preferences[PASSCODE] = passcode } }
}

