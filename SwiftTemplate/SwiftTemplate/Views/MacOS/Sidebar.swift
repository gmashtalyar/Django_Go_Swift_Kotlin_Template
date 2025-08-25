import SwiftUI

struct Sidebar: View {
    
    @Binding var sidebarSelection: SidebarSelection?
    
    var body: some View {
        List(SidebarSelection.allCases, id: \.self, selection: $sidebarSelection) { selection in
            Label(selection.displayName, systemImage: selection.iconName).tag(selection)
        }
        .listStyle(SidebarListStyle())
    }
}
