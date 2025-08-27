package com.example.kotlin_template.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.kotlin_template.Screen
import com.example.kotlin_template.viewModel.PasscodeDataStore
import kotlinx.coroutines.launch

@Composable
fun PasscodeSetScreen(navController: NavController){

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val dataStore = PasscodeDataStore(context)

    var input_01 by remember { mutableStateOf("") }
    var input_02 by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize().background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ){
        Spacer(modifier = Modifier.padding(25.dp))
        Text("Установите пароль", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.padding(25.dp))

        PasscodeInput("Введите пароль") { value ->
            input_01 = value
        }
        PasscodeInput("Подтвердите пароль") { value ->
            input_02 = value
        }

        Spacer(modifier = Modifier.padding(25.dp))

        TextButton(onClick = {
            println(input_01)
            println(input_02)

            if (input_01 == input_02) {
                scope.launch {
                    dataStore.savePasscodeData(passcode = input_01)
                    navController.navigate(Screen.Clients_Lists.route){
                        popUpTo("auth_logic") {
                            inclusive = true
                        }
                    }
                }

            } else {
                println("error error error ")
            }


        }) {Text("Установите пароль")}
    }
}



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PasscodeInput(label: String, onValueChange: (String) -> Unit) {
    var passcode: String by remember { mutableStateOf("") }
    TextField(
        value = passcode,
        onValueChange = {
            if (it.length <=4) {
                passcode = it
                onValueChange(it)
            }
        },
        modifier = Modifier.fillMaxWidth(),
        label = { Text(label) },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
        colors = TextFieldDefaults.textFieldColors(
            containerColor = Color.White,
            focusedIndicatorColor = Color.Transparent,
            unfocusedIndicatorColor = Color.Transparent,
            disabledIndicatorColor = Color.Transparent),
        singleLine = true,
    )
}



//@Preview(showBackground = true)
//@Composable
//fun PasscodeSetScreenPreview(){
//    PasscodeSetScreen()
//}