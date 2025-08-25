import SwiftUI

struct SetUpPINView: View {
    @State private var pin = ""
    @State private var confirmPin = ""
    @Binding var isPINVerified: Bool
    @EnvironmentObject var authViewModel: AuthViewModel
    @Binding var appState: AppState

    
    var body: some View {
        NavigationView {
            VStack {
                #if os(iOS)
                Text("Установите пароль").font(.title).padding()
                SecureField("Введите пароль", text: $pin).keyboardType(.numberPad).padding()
                SecureField("Подтвердите пароль", text: $confirmPin).keyboardType(.numberPad).padding()
                Button("Установите пароль") {
                    if pin.count == 4 && pin == confirmPin {
                        UserDefaults.standard.set(pin, forKey: "AppPIN")
                        isPINVerified = true
                        appState = .mainView
                    } else {print("Ошиблись в простой задаче, представьте как сложно было написать эту часть кода")}
                }.padding()
                Spacer()
                #endif
            }
        }
    }
}

//
//#Preview {
//    SetUpPINView()
//}

//struct SetUpPINView_Previews: PreviewProvider {
//    static var previews: some View {
//        SetUpPINView(isPINVerified: .constant(false), appState: .constant(.pinSetup))
//            .environmentObject(AuthViewModel()) // Assuming AuthViewModel needs to be injected
//    }
//}
