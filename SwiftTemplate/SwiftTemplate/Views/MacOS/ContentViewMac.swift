import SwiftUI

struct ContentViewMac: View {
    @State private var newMessage: String = ""  // what is it used for?
    @State private var appState: AppState = .initial
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var isPINVerified = false
    @State private var correctPIN = ""
    @State private var navigateToClientView: String? = nil
    @State private var sidebarSelection: SidebarSelection? = SidebarSelection.home
    
    
    var body: some View {
        NavigationSplitView {
            switch appState {
            case .initial, .pinSetup, .pinVerification:
                EmptySidebar()
            case .demo, .mainView, .pinOff:
                Sidebar(sidebarSelection: $sidebarSelection)
            }
        } detail: {
            switch appState {
            case .initial:
                LoginViewMac(appState: $appState, isPINVerified: $isPINVerified)
            case .demo:
                MainViewMac(appState: $appState, isPINVerified: $isPINVerified, sidebarSelection: $sidebarSelection)
            case .pinSetup:
                SetUpPINView(isPINVerified: $isPINVerified, appState: $appState)
            case .pinVerification:
                VerifyPINView(appState: $appState, isVerified: $isPINVerified, correctPIN: correctPIN)
            case .mainView:
                MainViewMac(appState: $appState, isPINVerified: $isPINVerified, sidebarSelection: $sidebarSelection)
            case .pinOff:
                MainViewMac(appState: $appState, isPINVerified: $isPINVerified, sidebarSelection: $sidebarSelection)

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
//        .onReceive(NotificationCenter.default.publisher(for: .navigateToClientView)) { notification in
//            if let clientID = notification.object as? String {
//                navigateToClientView = clientID
//            }
//        }
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
