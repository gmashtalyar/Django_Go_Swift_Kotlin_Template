package com.example.kotlin_template.view

import android.annotation.SuppressLint
import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.kotlin_template.Screen
import com.example.kotlin_template.dataStoreFB
import com.example.kotlin_template.network.ApiService
import com.example.kotlin_template.viewModel.DeviceTokenViewModel
import com.example.kotlin_template.viewModel.PasscodeDataStore
import com.example.kotlin_template.viewModel.PasscodePrefStore
import com.example.kotlin_template.viewModel.UserDataStore
import com.example.kotlin_template.viewModel.UserViewModel
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

@SuppressLint("UnusedMaterial3ScaffoldPaddingParameter")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(navController: NavController, userViewModel: UserViewModel, settings_status: String){

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val user_data_store = UserDataStore(context)
    val passcode_data_store = PasscodeDataStore(context)

    val dataStoreFB = context.dataStoreFB

    val saved_user_data by user_data_store.getUserData.collectAsState(initial = UserDataStore.UserDataStoreClass(
        id=0, email="", firstName="", lastName="", username="", apiUrl="", otdel="", directorId=0, department="",
        userGroup=""))
//    val saved_passcode_data by passcode_data_store.getPasscode.collectAsState(initial = "")

    val passcode_pref = PasscodePrefStore(context)
    val saved_passcode_pref by passcode_pref.getPasscodePref.collectAsState(initial = false)

    val token by remember {
        mutableStateOf("")
        derivedStateOf {
            runBlocking {
                dataStoreFB.data.first()[stringPreferencesKey("FMC_token")] ?: ""
            }
        }
    }

    Scaffold(
        bottomBar = { BottomBar(navController) }
    ) {
        Column(modifier = Modifier.padding(8.dp).background(Color.White).fillMaxWidth(),
            verticalArrangement = Arrangement.SpaceBetween, horizontalAlignment = Alignment.CenterHorizontally) {
            Spacer(modifier = Modifier.padding(25.dp))
            if (saved_user_data.email != "demo@fintechdocs.ru") {
                Spacer(modifier = Modifier.padding(25.dp))

                if (settings_status=="") { // ApiService.NotiSettingsJSON(user_id= 0, status_notifications = emptyList(), comments_notifications= 0, late_debt_notifications= 0, resolution_notifications= 0, email="", device_type = "android")
                    TextButton(
                        onClick = {
                            navController.navigate("notification_settings/${saved_user_data.id}/${saved_user_data.email}")
                        }
                    ) {
                        Text("Установить настройки оповещений")
                    }
                } else {
                    Spacer(modifier = Modifier.padding(25.dp))
                    Button(
                        onClick = {
                            try {
                                val deviceTokenViewModel = DeviceTokenViewModel()
                                val deviceJSON = ApiService.DeviceJSON(registration_id = token, device_type = "android",
                                    user_id = saved_user_data.id, email = saved_user_data.email)
                                deviceTokenViewModel.sendDeviceToken(api_path = "register_device/",
                                    deviceJSON = deviceJSON)
                                Log.d("Cloud Message", "Token sent to server successfully")
                                Log.d("Cloud Message", "${deviceJSON}")
                            } catch (e: Exception) { Log.e("Cloud Message", "Error sending token to server: ${e.message}") }
                        }
                    ) { Text("Запросить уведомления") }
                }

            }

            if (saved_passcode_pref==true) {
                Spacer(modifier = Modifier.weight(1f))
                Button(onClick = { scope.launch {
                    passcode_pref.falsePasscodePref()
                    navController.navigate("pin_setup"){
                        popUpTo("pin_setup") { inclusive = true } }
                }}) {Text("Установить пароль")}

            } else {
                Spacer(modifier = Modifier.weight(1f))

                Button(onClick = { scope.launch {
                    passcode_pref.falsePasscodePref()
                    navController.navigate("pin_setup"){
                        popUpTo("pin_setup") { inclusive = true } }
                }}) {Text("Изменить")}

                Spacer(modifier = Modifier.weight(1f))

                Button(onClick = { scope.launch { passcode_pref.truePasscodePref() } }) {Text("Отключить вход по паролю")}
            }

            Spacer(modifier = Modifier.weight(1f))
            Button(
                onClick = {
                    scope.launch {
                        val user_data_deferred = async {user_data_store.saveUserData(id=0, email="",
                            first_name="", last_name="", username="", api_url="", otdel="", director_id=0,
                            department="", user_group="") }
                        val passcode_data_deferred = async {passcode_data_store.savePasscodeData(passcode = "")}
                        user_data_deferred.await()
                        passcode_data_deferred.await()
                        userViewModel.login_result = UserViewModel.LoginResult.Initial
                        navController.navigate("auth_logic"){//Screen.Login_Form.route
                            popUpTo(Screen.Clients_Lists.route) { inclusive = true } }
                    }
                }, modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color.Red)
            ) { Text("Выйти") }

            Spacer(modifier = Modifier.padding(50.dp))

        }

    }
}


//@Preview
//@Composable
//fun SettingsScreenPreview() {
//    CreditTheme {
//        val navController = rememberNavController()
//        SettingsScreen(navController)
//    }
//}


