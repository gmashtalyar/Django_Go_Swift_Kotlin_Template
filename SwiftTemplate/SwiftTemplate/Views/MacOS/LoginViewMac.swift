import SwiftUI

struct LoginViewMac: View {
    @StateObject var viewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @Binding var appState: AppState
    @Binding var isPINVerified: Bool
    
    @State private var errorMessage = ""

    
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
                TLButton(title: "Войти", background: .blue) {login()}.padding()
                TLButton(title: "Демо версия", background: .black) {loginDemo()}.padding()
            }
            Spacer()
        }
    }
    
    private func login() {
        let lowercaseEmail = viewModel.email.lowercased()
        viewModel.loginUser(username: viewModel.username, password: viewModel.password, email: lowercaseEmail) {result in
            switch result {
            case .success(let user):
                print("Login successful. User \(user)")
                DispatchQueue.main.async {
                    authViewModel.isLoggedIn = true
                    appState = .pinSetup
                }
            case .failure(let error):
                DispatchQueue.main.async{
                    errorMessage = handleLoginError(error)
                }
            }
        }
    }
    
    private func loginDemo() {
        viewModel.loginUser(username: "mobile_demo", password: "gYJDFP4c", email: "demo@fintechdocs.ru") {result in
            switch result {
            case .success(let user):
                print("Login successful. User \(user)")
                DispatchQueue.main.async {
                    authViewModel.isLoggedIn = true
                    appState = .demo
                }
            case .failure(_):
                errorMessage = "Проверьте подключение к интернету."
            }
        }
    }
    
    private func handleLoginError(_ error: Error) -> String {
        if let loginError = error as? LoginError {
            switch loginError {
            case .invalidCredentials:
                return "Неверные учетные данные. Проверьте логин и пароль."
            case .networkError:
                return "Проверьте подключение к интернету."
            default:
                return "Произошла неизвестная ошибка. Попробуйте езе раз."
            }
        }
        return "Произошла ошибка. Попробуйте позже."
    }

}
