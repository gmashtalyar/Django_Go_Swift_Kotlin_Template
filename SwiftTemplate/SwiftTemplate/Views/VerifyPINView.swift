import SwiftUI

struct VerifyPINView: View {
    @State private var enteredPIN = ""
    @Binding var appState: AppState
    @Binding var isVerified: Bool
    let correctPIN: String

    var body: some View {
        NavigationView {
            VStack {
                #if os(iOS)
                Text("Введите пароль для приложения").font(.title).padding()
                SecureField("Пароль", text: $enteredPIN).keyboardType(.numberPad).padding()
                Button("Подтвердить") {
                    if enteredPIN == correctPIN {
                        appState = .mainView
                    } else {print("Wrong pin")}
                }
                .padding()
                Spacer()
                Button("Восстановить пароль") {appState = .initial}
                Spacer()
                #endif
            }
        }
    }
}
