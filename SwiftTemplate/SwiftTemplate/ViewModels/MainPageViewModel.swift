import Foundation
import Combine

class MainPageViewModel: ObservableObject {
    
    @Published var clients_model_data: [ClientsJson]?
    @Published var statuses: [String] = []

    init() {
        fetch(clients_type:"")
    }

    func fetch(clients_type: String) {
        
        guard let url = buildURL() else { return }
//        guard let url = URL(string: "https://www.XXXXXX.ru/swift/api_clients_swift/all") else { return }
        let task  = URLSession.shared.dataTask(with: url) { [weak self] data, _, error in

            guard let data = data, error == nil else { return }

            do {
                let clients_model_data = try JSONDecoder().decode([ClientsJson].self, from: data)
                DispatchQueue.main.async {
                    self?.clients_model_data = clients_model_data
                }
            } catch {print(error)}
        }
        task.resume()
    }
    
    
    private func buildURL() -> URL? {
        if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
           let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData) {
            return URL(string: "\(loggedInUser.api_url)swift/api_clients_swift/all/\(loggedInUser.id)")
        } else {return nil}
    }
    
    func fetch_statuses() {
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
                    print(data)
                }
            }
            task.resume()
        }
    }
    
}

