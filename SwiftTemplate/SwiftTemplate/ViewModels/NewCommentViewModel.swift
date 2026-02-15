import Foundation


class NewCommentViewModel: ObservableObject {
//    @Published var createdComment: NewCommentModel?
    @Published var error: Error?
    
    static let shared = NewCommentViewModel()
    
//    func createComment(commentType: String, comment: NewCommentModel, completion: @escaping(Result<NewCommentModel, Error>) -> Void) {
//        if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
//           let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData) {
//            guard let url = URL(string: "\(loggedInUser.api_url)swift/\(commentType)") else {return}
//            var request = URLRequest(url: url)
//            request.httpMethod = "POST"
//            
//            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
//            
//            do {
//                let jsonEncoder = JSONEncoder()
//                request.httpBody = try jsonEncoder.encode(comment)
//            } catch {
//                completion(.failure(error))
//                return
//            }
//            
//            URLSession.shared.dataTask(with:request) { data, response, error in
//                if let error = error {
//                    completion(.failure(error))
//                    return
//                }
//                guard let data = data else {
//                    completion(.failure(NSError(domain:"Data not found", code: 0, userInfo:nil)))
//                    return
//                }
//                do {
//                    let jsonDecoder = JSONDecoder()
//                    let createdComment = try jsonDecoder.decode(NewCommentModel.self, from:data)
//                    completion(.success(createdComment))
//                } catch {
//                    completion(.failure(error))
//                }
//            }.resume()
//        }
//    }
}





