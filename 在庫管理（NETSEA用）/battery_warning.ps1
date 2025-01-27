# バッテリーの状態を取得
$batteryStatus = (Get-WmiObject -Class Win32_Battery)

# バッテリーの残量が20%未満の場合に通知を出す
if ($batteryStatus.EstimatedChargeRemaining -lt 20) {
    # 通知を表示
    $notification = New-Object System.Windows.Forms.NotifyIcon
    $notification.Icon = [System.Drawing.SystemIcons]::Information
    $notification.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning
    $notification.BalloonTipTitle = "バッテリー警告"
    $notification.BalloonTipText = "バッテリー残量が20%未満です。充電してください。"
    $notification.Visible = $true
    $notification.ShowBalloonTip(3000)  # 通知を3秒間表示
}
