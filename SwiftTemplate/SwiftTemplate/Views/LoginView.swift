import SwiftUI

struct LoginView: View {
    @StateObject var viewModel = LoginViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    @Binding var appState: AppState
    @State private var keyboardHeight: CGFloat = 0
    @Binding var isPINVerified: Bool
    
    @State private var errorMessage = ""
    
    var body: some View {
#if os(iOS)
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(gradient: Gradient(colors: [.blue.opacity(0.2), .white]), startPoint: .top, endPoint: .bottom)
                    .edgesIgnoringSafeArea(.all)
                
                VStack(spacing: 20) {
                    // Logo and title
                    VStack(spacing: 20) {
                        Image("Logo").resizable().aspectRatio(contentMode: .fit)
                            .frame(height: 120)
                            .clipShape(RoundedRectangle(cornerRadius: 20))
                        
                        Text("Вход в систему")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.primary)
                    }
                    .padding(.top, 40)
                    
                    // Login form
                    VStack(spacing: 15) {
                        TextField("Логин", text: $viewModel.username)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocapitalization(.none)
                            .autocorrectionDisabled()
                            .padding(.horizontal)
                        
                        TextField("Рабочая почта", text: $viewModel.email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocapitalization(.none)
                            .autocorrectionDisabled()
                            .padding(.horizontal)
                        
                        SecureField("Пароль от СУДЗ", text: $viewModel.password)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .padding(.horizontal)
                        
                        if !errorMessage.isEmpty {
                            Text(errorMessage)
                                .font(.caption)
                                .foregroundColor(.red)
                                .padding(.horizontal)
                                .transition(.opacity)
                        }
                        
                        // Login button
                        TLButton(title: "Войти", background: .blue) {
                            login()
                        }
                        .frame(height: 40)
                        .padding(.horizontal)
                        .padding(.top, 10)
                        
                        // Demo button
                        TLButton(title: "Демо версия", background: .black) {
                            loginDemo()
                        }
                        .frame(height: 40)
                        .padding(.horizontal)
                    }
                    .padding(.vertical, 20)
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .shadow(radius: 5)
                    )
                    .padding(.horizontal)
                    
                    Spacer()
                }
                .offset(y: -keyboardHeight * 0.4) // Adjust view position when keyboard appears
                .animation(.easeOut(duration: 0.25), value: keyboardHeight)
            }
            .onAppear { setupKeyboardHandling() }
            .onDisappear { removeKeyboardHandling() }
            .fullScreenCover(isPresented: $authViewModel.isLoggedIn) {
                MainView(appState: $appState, isPINVerified: $isPINVerified)
            }
            .onTapGesture {
                UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
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
        NotificationCenter.default.addObserver(forName: UIResponder.keyboardWillShowNotification, object: nil, queue: .main) { notification in
            if let keyboardFrame = notification.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect {
                keyboardHeight = keyboardFrame.height
            }
        }
        
        NotificationCenter.default.addObserver(forName: UIResponder.keyboardWillHideNotification, object: nil, queue: .main) { _ in
            keyboardHeight = 0
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
                return "Произошла неизвестная ошибка. Попробуйте еще раз."
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

struct LoginView_Previews: PreviewProvider {
    @State private static var appState: AppState = .pinSetup
    @State private static var isPINVerified: Bool = false
    static var previews: some View {
        let authViewModel = AuthViewModel()
        authViewModel.isLoggedIn = false
        
        return Group {
            LoginView(appState: $appState, isPINVerified: $isPINVerified)
                .environmentObject(authViewModel)
        }
    }
}
