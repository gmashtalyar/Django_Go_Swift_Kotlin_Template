package com.example.kotlin_template.view

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusManager
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusOrder
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.kotlin_template.network.ApiService
import com.example.kotlin_template.viewModel.LoginError
import com.example.kotlin_template.viewModel.UserDataStore
import com.example.kotlin_template.viewModel.UserViewModel
import kotlinx.coroutines.launch


@Composable
fun LoginScreen(navController: NavController, userViewModel: UserViewModel) {

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val dataStore = UserDataStore(context)

    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    var loginError by remember { mutableStateOf("") }

    val passwordFocusRequester = FocusRequester()
    val focusManager: FocusManager = LocalFocusManager.current

    LaunchedEffect(userViewModel.login_result) {
        when (userViewModel.login_result) {
            is UserViewModel.LoginResult.Success -> {
                val user = (userViewModel.login_result as UserViewModel.LoginResult.Success).user
                scope.launch {
                    dataStore.saveUserData(id=user.id, email=user.email, first_name = user.first_name, last_name=user.last_name,
                        username = user.username, api_url=user.api_url, otdel=user.otdel, director_id = user.director_id,
                        department = user.department, user_group = user.user_group)
                    if (user.email != "demo@fintechdocs.ru") { navController.navigate("pin_setup") }
                }
            }
            is UserViewModel.LoginResult.Failure -> {
                loginError = when (val error = (userViewModel.login_result as UserViewModel.LoginResult.Failure).error) {
                    is LoginError.InvalidCredentials -> "Неверные учетные данные. Проверьте логин и пароль."
                    is LoginError.NetworkError -> "Проверьте подключение к интернету."
                    is LoginError.UnknownError -> "Произошла неизвестная ошибка. Попробуйте еще раз."
                } }
            else -> { // UserViewModel.LoginResult.Initial -> {
                println("Initial state")
            }
        }
    }


    Column(Modifier.navigationBarsPadding().imePadding().padding(24.dp)) {
        Image(modifier = Modifier.fillMaxWidth(), contentDescription = null, painter = painterResource(id = R.drawable.logo))
        Spacer(modifier = Modifier.padding(20.dp))

        TextInput(InputType.Name, value = name, onValueChange = {name = it}, keyboardActions = KeyboardActions(onNext = {
            // passwordFocusRequester.requestFocus()
        }))
        TextInput(InputType.Email, value = email, onValueChange = {email = it.lowercase()}, keyboardActions = KeyboardActions(onNext = {
            passwordFocusRequester.requestFocus()
        }))
        TextInput(InputType.Password, value = password, onValueChange = {password = it}, keyboardActions = KeyboardActions(onDone = {
            focusManager.clearFocus()
        }), focusRequester = passwordFocusRequester)


        if (loginError.isNotEmpty()) {
            Text(loginError, color = Color.Red, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(bottom = 16.dp))
        }


        Spacer(modifier = Modifier.padding(25.dp))
        Button(onClick = {
            val loginJSON = ApiService.LoginJSON(username = name, email = email, password = password)
            userViewModel.login_user(api_path="api_login_swift", loginJSON=loginJSON)
        }, modifier = Modifier.fillMaxWidth()) {
            Text("Войти", modifier = Modifier.padding(vertical=8.dp)) }
        Spacer(modifier = Modifier.padding(10.dp))
        Button(onClick = {
            val loginJSON = ApiService.LoginJSON(username = "mobile_demo", email = "demo@fintechdocs.ru", password = "XXXXXX")
            userViewModel.login_user(api_path="api_login_swift", loginJSON=loginJSON)
        }, modifier = Modifier.fillMaxWidth()) {
            Text("Демо версия", modifier = Modifier.padding(vertical=8.dp)) }
        Spacer(modifier = Modifier.padding(10.dp))
    }
}


sealed class InputType(
    val label: String,
    val icon: ImageVector,
    val keyboardOptions: KeyboardOptions,
    val visualTransformation: VisualTransformation
) {
    object Name: InputType(
        label = "Логин",
        icon = Icons.Default.Person,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
        visualTransformation = VisualTransformation.None
    )
    object Email: InputType(
        label = "Корпоративная почта",
        icon = Icons.Default.Email,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
        visualTransformation = VisualTransformation.None
    )
    object Password: InputType(
        label = "Пароль от XXXXXX",
        icon = Icons.Default.Lock,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done, keyboardType = KeyboardType.Password),
        visualTransformation = PasswordVisualTransformation()
    )
}



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TextInput(inputType: InputType, value: String, onValueChange: (String) -> Unit, focusRequester: FocusRequester? = null, keyboardActions: KeyboardActions) {

    TextField(
        value = value,
        onValueChange = { onValueChange(it) },
        modifier = Modifier.fillMaxWidth().focusOrder(focusRequester ?: FocusRequester()),
        leadingIcon = { Icon(imageVector = inputType.icon, contentDescription = null )},
        label = { Text(text= inputType.label) },
        colors = TextFieldDefaults.textFieldColors(
            containerColor = Color.White,
            focusedIndicatorColor = Color.Transparent,
            unfocusedIndicatorColor = Color.Transparent,
            disabledIndicatorColor = Color.Transparent
        ),
        singleLine = true,
        keyboardOptions = inputType.keyboardOptions,
        visualTransformation = inputType.visualTransformation,
        keyboardActions = keyboardActions
    )
}




//@Preview
//@Composable
//fun LoginScreenPreview () {
//    val navController = rememberNavController()
//    val userViewModel = UserViewModel()
//    LoginScreen(navController, userViewModel)
//}