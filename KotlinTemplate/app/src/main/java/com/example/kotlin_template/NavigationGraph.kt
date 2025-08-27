package com.example.kotlin_template

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.kotlin_template.view.*
import com.example.kotlin_template.viewModel.*



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NavigationGraph(commentsViewModel: CommentsViewModel, userViewModel: UserViewModel,
                    notificationSettingsViewModel: NotificationSettingsViewModel
) {
    val navController = rememberNavController()
    val context = LocalContext.current
    val user_data_store = UserDataStore(context)
    val passcode_data_store = PasscodeDataStore(context)
    val saved_user_data by user_data_store.getUserData.collectAsState(initial = UserDataStore.UserDataStoreClass(0, "", "", "", "", "", "", 0, "", ""))
    val saved_passcode_data by passcode_data_store.getPasscode.collectAsState(initial = "")
    var server_link: String = saved_user_data.apiUrl

    Scaffold() {innerPadding ->
        NavHost(modifier = Modifier.padding(innerPadding), navController = navController, startDestination = "auth_logic") {
            composable("auth_logic") {
                if (saved_user_data.email == "demo@fintechdocs.ru") { navController.navigate(Screen.Clients_Lists.route) }
                else if (saved_user_data.id == 0 && saved_user_data.username == "") {
                    LoginScreen(navController, userViewModel)
                }
                else if (saved_passcode_data == "") {
                    PasscodeSetScreen(navController)
                } else {
                    PasscodeInputScreen(navController)
                }
            }
            composable(Screen.Login_Form.route) {
                LoginScreen(navController, userViewModel)
            }
            composable("pin_setup") {
                PasscodeSetScreen(navController)
            }
            composable(Screen.Settings_Form.route) {
                SettingsScreen(navController, userViewModel, settings_status = notificationSettingsViewModel.error_message)
            }
            composable("document/{non_pdf}") { navBackStackEntry ->
                val non_pdf = navBackStackEntry.arguments?.getString("non_pdf")
                //val link = navBackStackEntry.arguments?.getString("link")
                if ( non_pdf != null) {
                    downloadFileScreen(non_pdf=non_pdf)
                } else { LoadingScreen() }
            }
            composable("notification_settings/{user_id}/{email}") {navBackStackEntry ->
                val user_id = navBackStackEntry.arguments?.getString("user_id")
                val email = navBackStackEntry.arguments?.getString("email")
                if (user_id != null && email != null) {
                    NotificationSettingsView(navController = navController, settings = notificationSettingsViewModel.noti_settings,
                        notificationSettingsViewModel = notificationSettingsViewModel, server_link = server_link, user_id = user_id, email = email)
                } else { LoadingScreen() }
            }
        }
    }
}
