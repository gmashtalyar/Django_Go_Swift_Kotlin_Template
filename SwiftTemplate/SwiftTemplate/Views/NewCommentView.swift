import SwiftUI

struct NewCommentView: View {
    
    let clientID: Int
    
    @State private var clientInn = 0
    @State private var author = 0
    @State private var comment = ""
    @State private var commentDate = ""
    
    let viewModel: NewCommentViewModel
    @Binding var commentType: String
    @Binding var isShowingNewCommentView: Bool
    
    var onCommentPublished: () -> Void
    
    var body: some View {
        
        Form {
            Section(header: Text("Новый комментарий")) {
                TextField("Комментарий", text: $comment, axis: .vertical)
                    .lineLimit(5)}
            
            Button("Опубликовать") {
                print("Current Comment Type: \(commentType)")
                if let userData = UserDefaults.standard.data(forKey: "LoggedInUserData"),
                   let loggedInUser = try? JSONDecoder().decode(UserModel.self, from: userData) {
                    
                    let dateFormatter = DateFormatter()
                    dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSSSSS"
                    commentDate = dateFormatter.string(from: Date())
                    
//                    let newComment = NewCommentModel(
//                        id: nil,
//                        clientInn: clientID,
//                        author: loggedInUser.id,
//                        comment: comment,
//                        commentDate: commentDate
//                    )
                    
//                    viewModel.createComment(commentType: commentType, comment: newComment) { result in
//                        print(commentType)
//                        switch result {
//                        case .success(let createdComment):
//                            print("Comment created successfully: \(createdComment)")
//                            self.isShowingNewCommentView = false
//                        case .failure(let error):
//                            print("Failed to create comment. Error: \(error)")
//                        }
//                    }
                }
                onCommentPublished()
            }
        }
    }
}

