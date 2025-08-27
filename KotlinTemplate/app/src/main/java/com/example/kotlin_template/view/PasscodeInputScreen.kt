package com.example.kotlin_template.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.example.kotlin_template.Screen
import com.example.kotlin_template.viewModel.PasscodeDataStore

@Composable
fun PasscodeInputScreen(navController: NavController){
    val context = LocalContext.current
    val passcode_data_store = PasscodeDataStore(context)
    val saved_passcode_data by passcode_data_store.getPasscode.collectAsState(initial = "")
    var input_01 by remember { mutableStateOf("") }


    Column(modifier = Modifier.fillMaxSize().background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.padding(25.dp))
        Text("Введите пароль для приложения", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.padding(25.dp))
        PasscodeInput("Введите пароль") { value ->
            input_01 = value
        }

        Spacer(modifier = Modifier.padding(25.dp))

        TextButton(
            onClick = {
                if (input_01 == saved_passcode_data) {
                    navController.navigate(Screen.Clients_Lists.route){
                        popUpTo("auth_logic") {
                            inclusive = true
                        }
                    }
                } else {
                    println("Error error error")
                }
            }
        ) {
            Text("Подтвердить")
        }

        Spacer(modifier = Modifier.padding(25.dp))

        TextButton(onClick = {
            navController.navigate(Screen.Login_Form.route){
                popUpTo(Screen.Login_Form.route) {
                    inclusive = true
                }
            }
        }
        ) { Text("Восстановить пароль") }
    }

}


@Preview
@Composable
fun PasscodeInputScreenPreview () {
    val navController = rememberNavController()
    PasscodeInputScreen(navController)
}
