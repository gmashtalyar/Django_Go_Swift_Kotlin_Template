import SwiftUI
import FirebaseMessaging

struct NotificationSettingsView: View {
    @StateObject var vm: UtilsViewModel
    @Environment(\.presentationMode) var presentationMode
    @State private var is_button_pressed: Bool = false {
        didSet {
            if is_button_pressed {
                presentationMode.wrappedValue.dismiss()
            }
        }
    }
    
    @State private var notification_settings: NotificationSettingsModel?
    @State private var status: Bool = true
    
    private func updateToggleStates(with settings: NotificationSettingsModel) {
        status = settings.status == 1
    }
    
    private func onAppearAction() {
        vm.fetchNotificationPreferences{ result in
            switch result {
            case .success(let settings):
                DispatchQueue.main.async {
                    notification_settings = notification_settings
                    updateToggleStates(with: settings)
                }
            case .failure(let error):
                print("Error fetching notification settings: \(error)")
            }
        }
    }
    
    var notificaiton_params: [String: Any] { return [
        "status": status ? 1 : 0
    ]}
    
    var body: some View {
        List {
            Section(header: Text("Статусы").font(.headline).padding(.vertical, 10).frame(maxWidth: .infinity, alignment: .leading)) {
                Toggle("Статус", isOn: $status).toggleStyle(SwitchToggleStyle(tint: .accentColor))
            }
            Button("Установить настройки") { if let token = Messaging.messaging().fcmToken {
                vm.sendNotificationPreferences(token: token, params: notificaiton_params)
                is_button_pressed = true}
            }
        }
        .onAppear(perform: onAppearAction)
    }
}
