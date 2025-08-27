package com.example.kotlin_template.view

import android.app.DownloadManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Environment
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.kotlin_template.viewModel.UserDataStore

fun openPdf(context: android.content.Context, pdfUrl: String) {
    val intent = Intent(Intent.ACTION_VIEW)
    intent.setDataAndType(Uri.parse(pdfUrl), "application/pdf")
    intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP

    try {
        context.startActivity(intent)
    } catch (e:Exception) {
        e.printStackTrace()
    }
}


@Composable
fun downloadFileScreen(non_pdf: String) {
    val context = LocalContext.current
    val user_data_store = UserDataStore(context)
    val saved_user_data by user_data_store.getUserData.collectAsState(initial = UserDataStore.UserDataStoreClass(
        id=0, email="", firstName="", lastName="", username="", apiUrl="", otdel="", directorId=0, department="",
        userGroup=""))
    val link: String = "${saved_user_data.apiUrl}Documents/Documents/$non_pdf"
    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ){
        Text(non_pdf, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(16.dp))
        Text("Это не pdf документ. Посмотреть в приложении его нельзя.", style = MaterialTheme.typography.headlineSmall)
        Text("Документ можно скачать на телефон и открыть в других приложениях.", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(8.dp))

        Button(
            onClick = { downloadFile(context, link) },
            modifier = Modifier.padding(8.dp)
        ) {
            Text("Скачать документ")
        }
    }
}


fun downloadFile(context: android.content.Context,  link: String) {


    val uri = Uri.parse(link)

    val request = DownloadManager.Request(uri)
        .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        .setTitle("Скачивание документа")
        .setDescription("Скачивание ${uri.lastPathSegment}")
        .setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, uri.lastPathSegment)

    val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
    downloadManager.enqueue(request)
}




//@Preview(showBackground=true)
//@Composable
//fun PdfScreenPreview() {
//    downloadFileScreen(fileURL = "https://www.credit-app.ru/Documents/Documents/Отчет_Контур_Фокуса_Город.pdf")
//}

