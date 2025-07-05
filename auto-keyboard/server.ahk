#Requires AutoHotkey v2.0+
Persistent

; Yêu cầu thư viện socket hỗ trợ cho v2, bạn cần có AutoHotkeySocket.ahk bản tương thích v2
#Include AutoHotkeySocket.ahk

port := 12345
server := TCPServer(port, OnClient)

MsgBox "Đang lắng nghe trên cổng " port

OnClient(socket) {
    data := ""
    while buf := socket.Recv(1024)
        data .= buf

    if data != ""
        SendText(data)  ; SendText dùng tốt hơn cho Unicode và input dài
    socket.Close()
}