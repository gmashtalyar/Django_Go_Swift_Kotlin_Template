import SwiftUI
#if os(iOS)
import UserNotifications
import FirebaseCore
import FirebaseMessaging
#endif


@main
struct SwiftTemplateApp: App {
    @StateObject var authViewModel = AuthViewModel()

    
#if os(iOS)
    @UIApplicationDelegateAdaptor private var appDelegate: AppDelegate
    var body: some Scene {
        WindowGroup {
            if UIDevice.current.userInterfaceIdiom == .pad {
                ContentViewMac().environmentObject(authViewModel)
            } else {
                ContentView()
                    .environmentObject(authViewModel)
                    .onAppear {
                        resetBadgeCount()
                }
            }
        }
    }
    
    func resetBadgeCount() {
        UNUserNotificationCenter.current().setBadgeCount(0)
    }
    
#elseif os(macOS)
    var body: some Scene {
        WindowGroup {
            ContentViewMac()
                .environmentObject(authViewModel)
        }
    }
#endif
    
}


#if os(iOS)
class AppDelegate: NSObject, UIApplicationDelegate {
    @StateObject var vm = UtilsViewModel()
    let gcmMessageIDKey = "gcm.message_id"

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        FirebaseApp.configure()
        // Config push notification
        Messaging.messaging().delegate = self
        UNUserNotificationCenter.current().delegate = self
        
//        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
//            if let error = error {
//                print("Error requesting notification permissions: \(error)")
//            }
//        }
        application.registerForRemoteNotifications()
        return true
    }
    
    func applicationDidBecomeActive(_ application: UIApplication) {
        resetBadgeCount()
    }
    
    func application(_ application: UIApplication, didReceiveRemoteNotification userInfo: [AnyHashable: Any],
                     fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
        if let messageID = userInfo[gcmMessageIDKey] {
            print("Message ID: \(messageID)")}
        print(userInfo)
        incrementBadgeCount()
        completionHandler(UIBackgroundFetchResult.newData)
    }
}

extension AppDelegate: MessagingDelegate {
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        let deviceToken:[String: String] = ["token": fcmToken ?? ""]
        print("Device token: ", deviceToken) // This token can be used for testing notifications on FCM
        vm.sendDeviceRegistrationRequest(token: fcmToken ?? "", type: "ios")
    }
}

extension AppDelegate : UNUserNotificationCenterDelegate {

    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        let userInfo = notification.request.content.userInfo
        if let messageID = userInfo[gcmMessageIDKey] {
            print("Message ID: \(messageID)")}
        print(userInfo)
        
        incrementBadgeCount()
        completionHandler([[.banner, .badge, .sound]])
    }
    
    func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    }
    func application(_ application: UIApplication, didFailToRegisterForRemoteNotificationsWithError error: Error) {
    }
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        let userInfo = response.notification.request.content.userInfo
        if let messageID = userInfo[gcmMessageIDKey] {
            print("Message ID from userNotificationCenter didReceive: \(messageID)")}
        if let clientID = response.notification.request.content.userInfo["clientID"] as? Int {
                NotificationCenter.default.post(name: .navigateToClientView, object: clientID)
            }
        print(userInfo)
        completionHandler()
    }
}

extension Notification.Name {
    static let navigateToClientView  = Notification.Name("navigateToClientView")
}

func incrementBadgeCount() {
    let notificationsCount = UserDefaults.standard.integer(forKey: "notificationsCount")
    let newCount = notificationsCount + 1
    UserDefaults.standard.set(newCount, forKey: "notificationsCount")
    UNUserNotificationCenter.current().setBadgeCount(newCount)

}

func resetBadgeCount() {
    DispatchQueue.main.async {
        UserDefaults.standard.set(0, forKey: "notificationsCount")
        UNUserNotificationCenter.current().setBadgeCount(0)
    }
}

#elseif os(macOS)
//class AppDelegate: NSObject, NSApplicationDelegate {
//    @StateObject var vm = UtilsViewModel()
//    let gcmMessageIDKey = "gcm.message_id"
//    func applicationDidFinishLaunching(_ notification: Notification) {
//        FirebaseApp.configure()
//        NSApplication.shared.registerForRemoteNotifications(matching: [.alert, .badge, .sound])
//    }
//    func application(_ application: NSApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
//        let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
//        print("Device token for macOS: \(token)")
//    }
//
//    func application(_ application: NSApplication, didFailToRegisterForRemoteNotificationsWithError error: Error) {
//        print("Failed to register for remote notifications: \(error)")
//    }
//}
#endif



