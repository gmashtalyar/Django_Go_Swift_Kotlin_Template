import Foundation

struct UserModel: Codable {
    let id: Int
    let username, email, firstName, lastName, otdel, department, user_group, api_url: String
    let director_id: Int

    enum CodingKeys: String, CodingKey {
        case id, username, email
        case firstName = "first_name"
        case lastName = "last_name"
        case otdel, director_id, department, user_group, api_url
    }
}




