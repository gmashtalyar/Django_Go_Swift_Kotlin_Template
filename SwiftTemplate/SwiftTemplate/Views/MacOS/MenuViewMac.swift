import SwiftUI
#if os(iOS)
import FirebaseMessaging
#endif

struct MenuViewMac: View {
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
            List{
                Section {
                    NavigationLink(destination: ClientsListView(clients_type: "new")){ Text("Новые заявки")}
                    NavigationLink(destination: ClientsListView(clients_type: "open")){ Text("Открытые лимиты")}
                    NavigationLink(destination: ClientsListView(clients_type: "late")){ Text("Просроченная ДЗ")}
                    NavigationLink(destination: ClientsListView(clients_type: "closed")){ Text("Закрытые клиенты")}
                    NavigationLink(destination: ClientsListView(clients_type: "all")){ Text("Все клиенты")}
                }
                Section {
                    NavigationLink(destination: NewClientView(viewModel: NewClientViewModel())){ Text("Новая заявка на лимит")}
                }
            }
        }
        .navigationTitle("Главная страница")
    }
}

