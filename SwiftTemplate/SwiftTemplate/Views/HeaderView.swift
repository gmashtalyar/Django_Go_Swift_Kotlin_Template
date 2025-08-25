import SwiftUI

struct HeaderView: View {
    let title: String
    let subtitile: String
    let angle: Double
    let background: Color
    
    var screenWidth: CGFloat {
        #if os(iOS)
        return UIScreen.main.bounds.width
        #elseif os(macOS)
        return NSScreen.main?.frame.width ?? 800
        #endif
    }
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 0)
                .foregroundColor(background)
                .rotationEffect(Angle(degrees: angle))
            
            VStack {
                Text(title)
                    .font(.system(size: 50))
                    .foregroundColor(Color.white)
                    .bold()

                Text(subtitile)
                    .font(.system(size: 30))
                    .foregroundColor(Color.white)
                    .lineLimit(2)
                    .minimumScaleFactor(0.5)
            }
            .padding(.top, 80)
        }
        .frame(width: screenWidth * 3, height: 350)
        .offset(y:-150)
        
    }
}
