import Foundation
import Combine

class DocumentViewModel: ObservableObject {
    
    func make_url() -> String? {
        if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
           let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData) {
            return loggedInUser.api_url
        } else { return nil }
    }

    
    
}
