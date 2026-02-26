import SwiftUI

enum LoginError: Error {
    case invalidCredentials
    case networkError
    case unknown
}

struct LoginActions {
    let viewModel: LoginViewModel
    let authViewModel: AuthViewModel
    let onError: (String) -> Void

    func login(appState: Binding<AppState>) {
        let lowercaseEmail = viewModel.email.lowercased()
        viewModel.loginUser(username: viewModel.username, password: viewModel.password, email: lowercaseEmail) { result in
            switch result {
            case .success(let user):
                print("Login successful. User \(user)")
                DispatchQueue.main.async {
                    authViewModel.isLoggedIn = true
                    appState.wrappedValue = .pinSetup
                }
            case .failure(let error):
                DispatchQueue.main.async {
                    onError(handleLoginError(error))
                }
            }
        }
    }

    func loginDemo(appState: Binding<AppState>) {
        viewModel.loginUser(username: "mobile_demo", password: "gYJDFP4c", email: "demo@fintechdocs.ru") { result in
            switch result {
            case .success(let user):
                print("Login successful. User \(user)")
                DispatchQueue.main.async {
                    authViewModel.isLoggedIn = true
                    appState.wrappedValue = .demo
                }
            case .failure:
                DispatchQueue.main.async {
                    onError("Проверьте подключение к интернету.")
                }
            }
        }
    }

    func handleLoginError(_ error: Error) -> String {
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
}
