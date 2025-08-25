import Foundation
import UserNotifications
import SwiftUI

class UtilsViewModel: ObservableObject {
    @Published var hasPermission = false
    @Published var forbiddenPermission = false
    @Published var settings_data: NotificationSettingsModel?
    @Published var statuses: [String] = []
    @Published var selectedStatuses: Set<String> = []

    func fetchStatuses() {
        if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
           let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData),
           let url = URL(string: "\(loggedInUser.api_url)swift/statuses_list") {
            
            let task = URLSession.shared.dataTask(with: url) { [weak self] data, _, error in
                guard let data = data, error == nil else { return }
                do {
                    let statuses = try JSONDecoder().decode([String].self, from: data)
                    DispatchQueue.main.async {
                        self?.statuses = statuses
                    }
                } catch {
                    print("Error decoding statuses: \(error)")
                }
            }
            task.resume()
        }
    }
    
    func getAuthStatus() async {
        let status = await UNUserNotificationCenter.current().notificationSettings()
        
        DispatchQueue.main.async {
            switch status.authorizationStatus {
            case .authorized, .provisional, .ephemeral:
                self.hasPermission = true
            case .denied:
                self.hasPermission = false
                self.forbiddenPermission = true
            default:
                self.hasPermission = false}
        }
    }
    
    #if os(iOS)
        func requestNotificationPermission() async {
            do {
                let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
                let permission = try await UNUserNotificationCenter.current().requestAuthorization(options: authOptions)
                DispatchQueue.main.async {self.hasPermission = permission}
                await UIApplication.shared.registerForRemoteNotifications()
            } catch {print(error.localizedDescription)}}
    #endif
    
    func sendDeviceRegistrationRequest(token: String, type: String) {
        guard let url = URL(string: "https://www.credit-app.ru/swift/register_device/") else { return }
        if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
           let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData) {
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            
            let requestBody: [String: Any] = ["registration_id": token, "device_type": type, "user_id": loggedInUser.id, "email": loggedInUser.email]
            if let jsonData = try? JSONSerialization.data(withJSONObject: requestBody) {
                request.httpBody = jsonData
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")}
            
//            let parameters: [String: Any] = ["registration_id": token, "device_type": type, "user_id": loggedInUser.id, "email": loggedInUser.email]
//            request.httpBody = parameters.percentEncoded()
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error)")
                } else if let data = data {print("Response: \(String(data: data, encoding: .utf8) ?? "")")}
            }.resume()}}
    
    func sendNotificationPreferences(token: String, comment_params: [String: Any], status_params: [String]) {
        guard let url = URL(string: "https://www.credit-app.ru/swift/notification_settings") else {return}
        if let user_data = UserDefaults.standard.data(forKey: "LoggedInUserData"),
           let logged_in_user = try? JSONDecoder().decode(UserModel.self, from: user_data) {
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            
            var requestBody: [String: Any] = ["email": logged_in_user.email, "user_id": logged_in_user.id, "device_type": "ios"]
            requestBody.merge(comment_params) { (_, new) in new }
            let statusParamsDict: [String: [String]] = ["status_notifications": status_params]
            requestBody.merge(statusParamsDict) { (_, new) in new }

            if let jsonData = try? JSONSerialization.data(withJSONObject: requestBody) {
                request.httpBody = jsonData
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            }
                        
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {print("Error: \(error)")} else if let data = data {print("Response: \(String(data: data, encoding: .utf8) ?? "")")}}.resume()
        }}
    
    func fetchNotificationPreferences(completion: @escaping (Result<NotificationSettingsModel, Error>) -> Void){
        if let user_data = UserDefaults.standard.data(forKey: "LoggedInUserData"),
        let logged_in_user = try? JSONDecoder().decode(UserModel.self, from: user_data) {
            guard let url = URL(string: "https://www.XXXXXXX.ru/swift/share_preferences/\(logged_in_user.id)/\(logged_in_user.email)/ios") else {return}
            
            let task = URLSession.shared.dataTask(with: url) {[weak self] data, _, error in
                guard let data = data, error == nil else {
                    completion(.failure(NSError(domain: "Error", code: 1, userInfo: [NSLocalizedDescriptionKey:"notification settings fetching error"])))
                    return
                }
                do {
                    let settings = try JSONDecoder().decode(NotificationSettingsModel.self, from: data)
                    DispatchQueue.main.async {
                        self?.settings_data = settings
                        self?.selectedStatuses = Set(settings.status_notifications)
                        completion(.success(settings))
                    }
                } catch {completion(.failure(error))}}
            task.resume()} else{
                completion(.failure(NSError(domain: "Error", code: 2, userInfo: [NSLocalizedDescriptionKey:"notification settings error"])))
            }}
    
    
}


extension Dictionary {
    func percentEncoded() -> Data? {
        return map { key, value in
            let escapedKey = "\(key)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            let escapedValue = "\(value)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            return escapedKey + "=" + escapedValue
        }
        .joined(separator: "&")
        .data(using: .utf8)}}

extension CharacterSet {
    static let urlQueryValueAllowed: CharacterSet = {
        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "&")
        return allowed
    }()}


