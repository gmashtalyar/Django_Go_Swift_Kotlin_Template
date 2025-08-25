import SwiftUI
import PDFKit

struct DocumentView: View {
    let pdfURL: URL
    
    var body: some View {
        if pdfURL.pathExtension.lowercased() == "pdf" {
            PDFKitView(url: pdfURL)
        } else {
            List {
                Section() {
                    Text("Это не pdf документ. Просмотреть в приложении его нельзя.")
                    Text("Документ можно скачать на телефон и открыть в других приложениях.")
                }
                Section(header: Text("Документ").font(.headline).padding(.vertical, 10).frame(maxWidth: .infinity, alignment: .leading)) {
                    Button("Открыть файл") {
                        shareFile(pdfURL)
                    }
                }
            }
        }
    }
    
    private func shareFile(_ url: URL) {
        #if os(iOS)
        let activityViewController = UIActivityViewController(activityItems: [url], applicationActivities: nil)
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
            let window = windowScene.windows.first(where: { $0.isKeyWindow}) {
                window.rootViewController?.present(activityViewController, animated: true, completion: nil)
        }
        #elseif os(macOS)
        let _ = NSWorkspace.shared.open(url)
        #endif
    }
}


struct PDFViewer: View {
    let url: URL
    var body: some View {
        PDFKitView(url: url)
    }
}


#if os(iOS)
struct PDFKitView: UIViewRepresentable {
    let url: URL
    
    func makeUIView(context: Context) -> PDFView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        return pdfView
    }
    
    func updateUIView(_ uiView: PDFView, context: Context) {
        if let pdfDocument = PDFDocument(url: url) {
            uiView.document = pdfDocument
        }
    }
}
#elseif os(macOS)
struct PDFKitView: NSViewRepresentable {
    let url: URL
    
    func makeNSView(context: Context) -> PDFView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        return pdfView
    }
    
    func updateNSView(_ nsView: PDFView, context: Context) {
        if let pdfDocument = PDFDocument(url: url) {
            nsView.document = pdfDocument
        }
    }
}
#endif

//struct DocumentView_Previews: PreviewProvider {
//    static var previews: some View {
//        DocumentView(pdfURL: URL(string: "http://127.0.0.1:8000/Documents/Documents/Приказ_на_право_подписи_2023.pdf")!)
//    }
//}
