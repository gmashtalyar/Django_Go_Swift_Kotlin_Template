import Foundation

enum SidebarSelection: Identifiable, CaseIterable, Hashable {
    case home
    case statuses
    case settings
    
    var id: String {
        switch self {
        case .home:
            "home"
        case .statuses:
            "statuses"
        case .settings:
            "settings"
        }
    }
    
    var displayName: String {
        switch self {
        case .home:
            "Главная страница"
        case .statuses:
            "Статусы заявок"
        case .settings:
            "Настройки"
        }
    }
    
    var iconName: String {
        switch self {
        case .home:
            "house"
        case .statuses:
            "list.bullet"
        case .settings:
            "gearshape"
        }
    }
    
    static var allCases: [SidebarSelection] {
        [.home, .statuses, .settings]
    }
    
    
}
