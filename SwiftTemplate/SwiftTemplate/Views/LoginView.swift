
import SwiftUI

struct LoginView: View {
    @StateObject var viewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @Binding var appState: AppState
    @State private var isKeyboardVisible = false
    @Binding var isPINVerified: Bool
    
    @State private var errorMessage = ""
    
    var body: some View {
#if os(iOS)
        NavigationView {
            VStack {
                Image("Logo")
                Form {
                    TextField("Логин", text: $viewModel.username).textFieldStyle(DefaultTextFieldStyle())
                        .autocapitalization(.none)
                        .autocorrectionDisabled()
                    TextField("Рабочая почта", text: $viewModel.email).textFieldStyle(DefaultTextFieldStyle())
                    #if os(iOS)
                        .autocapitalization(.none)
                    #endif
                        .autocorrectionDisabled()
                    SecureField("Пароль от XXXXXXXX", text: $viewModel.password).textFieldStyle(DefaultTextFieldStyle())
                    
                    if !errorMessage.isEmpty {
                        Text(errorMessage).font(.caption).foregroundColor(.red).padding(.bottom, 8)
                    }
                    
                    TLButton(title: "Войти", background: .blue) {login()}.padding()
                    TLButton(title: "Демо версия", background: .black) {
                        loginDemo()
                    }.padding()
                
            }

                VStack {
                    Text("")
                }
                .padding(.bottom, 50)
                Spacer()
            }
            .onAppear{ setupKeyboardHandling()}
            .onAppear { removeKeyboardHandling() }
            .fullScreenCover(isPresented: $authViewModel.isLoggedIn) {
                MainView(appState: $appState, isPINVerified: $isPINVerified)
            }
        }
#endif
    }
#if os(iOS)
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
    
    private func setupKeyboardHandling() {
        NotificationCenter.default.addObserver(forName: UIResponder.keyboardWillShowNotification, object: nil, queue: .main) { _ in
            isKeyboardVisible = true  // Keyboard is visible
        }
        
        NotificationCenter.default.addObserver(forName: UIResponder.keyboardWillHideNotification, object: nil, queue: .main) { _ in
            isKeyboardVisible = false  // Keyboard is hidden
        }
    }
    
    private func removeKeyboardHandling() {
        NotificationCenter.default.removeObserver(self, name: UIResponder.keyboardWillShowNotification, object: nil)
        NotificationCenter.default.removeObserver(self, name: UIResponder.keyboardWillHideNotification, object: nil)
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
#endif
}

enum LoginError: Error {
    case invalidCredentials
    case networkError
    case unknown
}


//#Preview {
//    LoginView()
//}
