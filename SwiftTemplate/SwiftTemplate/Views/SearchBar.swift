import SwiftUI

struct SearchBar: View {
    @Binding var text: String
    let placeholder: String
    
    var body: some View {
        HStack {
            TextField(placeholder, text: $text)
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
            #if os(iOS)
                .background(Color(.systemGray5))
            #endif
                .cornerRadius(10)
                .padding(.horizontal, 15)
            
            if !text.isEmpty {
                Button(action: {
                    text = ""
                }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.gray)
                }
                .padding(.trailing, 10)
                .transition(.move(edge: .trailing))
//                .animation(.default)
            }
        }
    }
}
