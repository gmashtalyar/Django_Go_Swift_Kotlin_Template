import SwiftUI
#if os(iOS)
import FirebaseMessaging
#endif

struct MainViewMac: View {
    @ObservedObject var viewModel = MainPageViewModel()
    @StateObject var loginviewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var isPINSetupComplete = false
    @Binding var appState: AppState
    @StateObject var vm = UtilsViewModel()
    //    @State private var statuses: [String] = []
    @Binding var isPINVerified: Bool
    
    @Binding var sidebarSelection: SidebarSelection?
    
    var body: some View {
        Group {
            switch sidebarSelection {
            case .home:
                MenuViewMac(appState: $appState, isPINVerified: $isPINVerified)
            case .statuses:
                StatusesViewMac(appState: $appState, isPINVerified: $isPINVerified)
            case .settings:
                SettingsViewMac(appState: $appState, isPINVerified: $isPINVerified)
            default:
                Text("Сделайте выбор раздела слева.")
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
