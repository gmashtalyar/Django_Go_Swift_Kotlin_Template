import SwiftUI
#if os(iOS)
import FirebaseMessaging
#endif

struct SettingsViewMac: View {
    @ObservedObject var viewModel = MainPageViewModel()
    @StateObject var loginviewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var isPINSetupComplete = false
    @Binding var appState: AppState
    @StateObject var vm = UtilsViewModel()
    //    @State private var statuses: [String] = []
    @Binding var isPINVerified: Bool
    
    var body: some View {
        NavigationStack {
            VStack {
                if appState != .demo {
                    Spacer()
                    Text("Разрешение на оповещения: \(vm.hasPermission ? "Да" : "Нет")")
                    Text("\(vm.forbiddenPermission ? "Вы запретели оповещения в настройках устройства" : "")").bold()
                    Spacer()
                    
                    if vm.hasPermission {
                        NavigationLink(destination: NotificationSettingsView(vm: vm)){ Text("Настройки оповещений")}
                        Spacer()
                    }
                    
                    
                    #if os(iOS)
                    if vm.hasPermission == false && vm.forbiddenPermission == false {
                        Button { Task {
                            await vm.requestNotificationPermission()
                            if let token = Messaging.messaging().fcmToken {
                                vm.sendDeviceRegistrationRequest(token: token, type: "ios")}}
                        } label: {Text("Подключить уведомления")}
                            .padding().buttonStyle(.bordered).disabled(vm.hasPermission) // off in the other code
                            .task {await vm.getAuthStatus()}
                        Spacer()
                    }
                    #endif
                    
                    
                    if UserDefaults.standard.bool(forKey: "noPin") {
                        Button(action: {
                            UserDefaults.standard.set(false, forKey: "noPin")
                            appState = .pinSetup
                        }) { Text("Установить пароль")}
                            .padding().foregroundColor(.white).frame(width: 350, height: 50).background(Color.blue).cornerRadius(10)

                    } else {
                        Button(action: {
                            appState = .pinSetup
                        }) { Text("Изменить пароль")}
                            .padding().foregroundColor(.white).frame(width: 350, height: 50).background(Color.blue).cornerRadius(10)
                        
                        Button(action: {
                            UserDefaults.standard.set(true, forKey: "noPin")
                            UserDefaults.standard.removeObject(forKey: "AppPIN")
                            appState = .pinOff
                        }) { Text("Отключить вход по паролю")}
                            .padding().foregroundColor(.white).frame(width: 350, height: 50).background(Color.blue).cornerRadius(10)
                    }
                }
                
                Button(action: { loginviewModel.logoutUser() { result in
                        switch result {
                        case .success():
                            if let bundleID = Bundle.main.bundleIdentifier { UserDefaults.standard.removePersistentDomain(forName: bundleID)}
                            DispatchQueue.main.async {
                                authViewModel.isLoggedIn = false
                                appState = .initial}
                        case .failure(let error):
                            print("Logout failed. Error: \(error)")
                        }}}) {Text("Выйти").foregroundColor(.white).frame(width: 350, height: 50).background(Color.pink).cornerRadius(10)}
                    }
            .navigationTitle("Настройки")
        }
    }
}
