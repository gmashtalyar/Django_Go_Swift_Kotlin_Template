package com.example.kotlin_template.view

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.example.kotlin_template.Screen

@Composable
fun BottomBar(navController: NavController){

    Row(modifier = Modifier.padding(8.dp).background(Color.White).fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically

    ) {
        Box(modifier = Modifier.height(48.dp).clickable(onClick = {
            navController.navigate(Screen.Settings_Form.route)
        })) { Text("Настройки",fontWeight = FontWeight.Bold, fontSize = 13.sp) }
    }
}


@Preview()
@Composable
fun BottomBarPreview() {
    val navController = rememberNavController()
    BottomBar(navController)
}
