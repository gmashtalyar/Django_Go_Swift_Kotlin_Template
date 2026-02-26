import SwiftUI

struct LoginViewMac: View {
    @StateObject var viewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @Binding var appState: AppState
    @Binding var isPINVerified: Bool

    @State private var errorMessage = ""

    private var actions: LoginActions {
        LoginActions(viewModel: viewModel, authViewModel: authViewModel) { self.errorMessage = $0 }
    }

    var body: some View {
        VStack {
            Image("Logo")
            Form {
                TextField("Логин", text: $viewModel.username).textFieldStyle(DefaultTextFieldStyle()).autocorrectionDisabled()
                    #if os(iOS)
                        .autocapitalization(.none)
                    #endif
                TextField("Рабочая почта", text: $viewModel.email).textFieldStyle(DefaultTextFieldStyle()).autocorrectionDisabled()
                    #if os(iOS)
                        .autocapitalization(.none)
                    #endif
                SecureField("Пароль от СУДЗ", text: $viewModel.password).textFieldStyle(DefaultTextFieldStyle())
                if !errorMessage.isEmpty { Text(errorMessage).font(.caption).foregroundColor(.red).padding(.bottom, 8)}
                TLButton(title: "Войти", background: .blue) { actions.login(appState: $appState) }.padding()
                TLButton(title: "Демо версия", background: .black) { actions.loginDemo(appState: $appState) }.padding()
            }
            Spacer()
        }
    }
}
