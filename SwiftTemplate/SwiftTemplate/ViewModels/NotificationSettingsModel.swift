import Foundation


struct NotificationSettingsModel: Codable {
    let user_id: Int
    let email: String
    let status: Int
    
    enum CodingKeys: String, CodingKey {
        case user_id = "user_id"
        case email = "email"
        case status = "status"
    }
}
