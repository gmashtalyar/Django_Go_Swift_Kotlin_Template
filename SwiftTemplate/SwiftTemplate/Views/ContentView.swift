import SwiftUI

struct ContentView: View {
    @State private var appState: AppState = .initial
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var isPINVerified = false
    @State private var correctPIN = ""
    @State private var navigateToClientView: String? = nil

    var body: some View {
        NavigationView {
            switch appState {
            case .initial:
                LoginView(appState: $appState, isPINVerified: $isPINVerified)
            case .demo:
                MainView(appState: $appState, isPINVerified: $isPINVerified)
            case .pinSetup:
                SetUpPINView(isPINVerified: $isPINVerified, appState: $appState)
            case .pinVerification:
                VerifyPINView(appState: $appState, isVerified: $isPINVerified, correctPIN: correctPIN)
            case .mainView:
                MainView(appState: $appState, isPINVerified: $isPINVerified)
            case .pinOff:
                MainView(appState: $appState, isPINVerified: $isPINVerified)
            }
        }
        .onAppear {
            if UserDefaults.standard.bool(forKey: "noPin") {
                appState = .pinOff
            } else if let storedPIN = UserDefaults.standard.string(forKey: "AppPIN") {
                appState = .pinVerification
                correctPIN = storedPIN
            } else if let savedAppState = UserDefaults.standard.string(forKey: "AppState") {
                appState = mapStringToAppState(savedAppState)
            } else { appState = .initial }
        }
        #if os(iOS)
        .onReceive(NotificationCenter.default.publisher(for: .navigateToClientView)) { notification in
            if let clientID = notification.object as? String {
                navigateToClientView = clientID
            }
        }
        #endif
        
    }
    
    func mapStringToAppState(_ stringValue: String) -> AppState {
        switch stringValue {
        case "initial":
            return .initial
        case "pinSetup":
            return .pinSetup
        case "pinVerification":
            return .pinVerification
        case "mainView":
            return .mainView
        case "pinOff":
            return .pinOff
        default:
            return .initial
        }
    }
}


enum AppState {
    case initial
    case demo
    case pinSetup
    case pinVerification
    case mainView
    case pinOff
}


//#Preview {
//    ContentView()
//}
