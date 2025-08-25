import Foundation


class LoginViewModel: ObservableObject {
    @Published var username: String = ""
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var loggedInUser: UserModel?
    @Published var error: Error?
    
    static let shared = LoginViewModel()
    
    func loginUser(username: String, password: String, email: String, completion: @escaping (Result<UserModel, Error>) -> Void) {
        guard let url = URL(string: "https://www.XXXXXXX.ru/swift/api_login_swift") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let credentials = ["username": username ,"email": email, "password": password]

        do {
            let jsonEncoder = JSONEncoder()
            request.httpBody = try jsonEncoder.encode(credentials)
        } catch {
            completion(.failure(error))
            return
        }
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(LoginError.networkError))
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                completion(.failure(LoginError.unknown))
                return
            }
            
            guard let data = data else {
                completion(.failure(LoginError.unknown))
                return
            }
            
            if httpResponse.statusCode == 401 {
                completion(.failure(LoginError.invalidCredentials))
                return
            }
            
            do {
                let jsonDecoder = JSONDecoder()
                let loggedInUser = try jsonDecoder.decode(UserModel.self, from: data)
                completion(.success(loggedInUser))
                UserDefaults.standard.set(data, forKey: "LoggedInUserData")
            } catch {
                completion(.failure(LoginError.unknown))
            }
        }.resume()
    }
    
    func logoutUser(completion: @escaping ((Result<Void, Error>) -> Void)) {
        UserDefaults.standard.removeObject(forKey: "LoggedInUserData")
        guard let url = URL(string: "https://www.XXXXXXX.ru/swift/api_logout_swift") else {
            completion(.failure(NSError(domain:"Invalid URL", code: 0, userInfo: nil)))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        URLSession.shared.dataTask(with: request) { _, _, error in
            if let error = error {
                completion(.failure(error))
            } else {
                UserDefaults.standard.removeObject(forKey: "LoggedInUserData")
                if let bundleID = Bundle.main.bundleIdentifier {
                    UserDefaults.standard.removePersistentDomain(forName: bundleID)
                }
                completion(.success(()))
            }
        }.resume()
    }
}
    
