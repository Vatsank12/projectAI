# VigilantAI - New Features Quick Start Guide

## 🚀 Getting Started

After the latest update, VigilantAI now includes several professional features designed to enhance your system monitoring experience.

---

## 👤 User Profile Management

### Access Profile
1. Click **👤 Profile** in the left navigation menu
2. Your profile information will load with three tabs: **Personal**, **Preferences**, and **Security**

### Personal Tab
- **Full Name**: Update your display name
- **Email**: Add your email address
- **Bio**: Write a brief bio about yourself
- **Save Changes**: Click to persist your personal information

*Your data is saved to browser storage for quick access across sessions.*

### Preferences Tab
- **Theme Preference**: Choose between Dark (Cyberpunk), Light, or Auto
- **Notification Sound**: Toggle audio alerts for system notifications
- **Email Notifications**: Enable/disable email notifications preference
- **Save Preferences**: Store your preferred settings

### Security Tab
- **Change Password**: Update your account password
- **Password Validation**: 
  - Confirm your current password
  - Enter new password (minimum 6 characters)
  - Confirm new password matches
- **Last Login**: View when you last accessed the dashboard

---

## 📊 Advanced Analytics

### Access Analytics Dashboard
1. Click **📈 Analytics** in the left navigation menu
2. View real-time trends and system statistics

### CPU & Memory Trends
- **CPU Usage Trend Chart**: Real-time CPU usage visualization
- **Memory Trend Chart**: Real-time memory usage visualization
- Both charts display the last 30 seconds of data with smooth animations

### System Statistics
Four key metrics displayed:
- **Avg CPU Usage**: Average CPU percentage over the monitoring period
- **Peak CPU Usage**: Maximum CPU spike recorded
- **Avg Memory Usage**: Average memory consumption
- **Peak Memory Usage**: Maximum memory spike recorded

*Statistics update every 2 seconds automatically*

---

## 📋 System Reports

### Access Reports
1. Click **📋 Reports** in the left navigation menu
2. Select from three report categories using tabs

### Performance Report
- **Current CPU Usage**: Real-time CPU percentage
- **Average CPU (Last Hour)**: Smoothed CPU average
- **Current Memory Usage**: Real-time memory percentage
- **Average Memory (Last Hour)**: Smoothed memory average
- Visual progress bars show metric ratios

### Security Report
- **Files Scanned**: Total number of files scanned
- **Threats Detected**: Count of identified threats
- **Last Scan**: Timestamp of most recent scan

### Health Report
- **Overall Health Score**: Calculated from CPU/Memory/Disk metrics
- **System Uptime**: Total time system has been running
- **System Status**: Health indicator (Healthy/Warning/Critical)

---

## 🔔 Notifications Center

### Access Notifications
1. Click **🔔 Notifications** in the left navigation menu
2. View all system notifications with timestamps

### Notification Types
- **Success** (Green): Successful operations
- **Warning** (Orange): Warning messages
- **Error** (Red): Error messages
- **Info** (Blue): Information messages

### Notification Actions
- **Clear All**: Remove all notifications from the list
- Notifications are **color-coded** by type for quick identification
- **Timestamps** show exact time of notification
- **Unread** notifications have special highlighting

### Managing Notifications
1. Notifications are displayed newest-first
2. Up to 50 most recent notifications shown
3. Clear all with one click
4. Sound alerts can be toggled in Profile > Preferences

---

## 🔊 Sound Alerts

### Enable/Disable Sound Alerts
1. Go to **👤 Profile**
2. Click **Preferences** tab
3. Toggle **Notification Sound** switch
4. Click **Save Preferences**

### Sound Alert Behavior
- Plays on warning, error, and success notifications
- 800Hz sine wave tone (non-intrusive)
- Very short duration (100ms)
- Only plays if enabled in preferences

---

## 📱 Using the Dashboard

### Navigation
**New Sections (Left Menu):**
- 📈 **Analytics** - Advanced metrics and trends
- 📋 **Reports** - Comprehensive system reports
- 🔔 **Notifications** - Notification management
- 👤 **Profile** - User account and preferences

**Existing Sections:**
- 📊 Dashboard - Main overview
- ⚙️ Processes - Process management
- 🔍 Scanner - File security scanning
- 🚨 Alerts - Security alerts
- ⚙️ Settings - System configuration

### Mobile Responsive
- All new sections are fully responsive
- Optimized layout for tablets and mobile devices
- Touch-friendly controls
- Automatic layout adaptation

---

## 💾 Data Persistence

### What Gets Saved
**Browser Storage (localStorage):**
- Full Name
- Email Address
- Bio/About
- Theme Preference
- Sound Alert Setting
- Email Notification Preference

**Backend (SQLite Database - Optional):**
- User profiles
- Notifications history
- Scan history
- Alert history

### Clearing Data
- Profile data persists until manually changed
- Notifications clear with "Clear All" button
- Browser cache can be cleared to reset all saved preferences

---

## 🎨 Customization Options

### Theme Selection
Choose your preferred theme in Profile > Preferences:
1. **Dark (Cyberpunk)** - Default dark theme with neon colors
2. **Light** - Light theme for daytime use
3. **Auto** - Automatically switches based on system preference

### Notification Preferences
- Sound alerts for system events
- Email notification opt-in
- Notification center management

### Profile Customization
- Set your full name
- Add email address
- Write a personal bio
- Change password

---

## 🔍 Monitoring Tips

### Using Analytics
1. Check **Analytics** regularly to identify trends
2. Look for **Peak Usage** patterns to understand workload
3. Compare **Average** vs **Peak** to assess system stress
4. Use trends to predict performance issues

### Interpreting Reports
1. **Performance**: Look for consistent high CPU/Memory = optimization needed
2. **Security**: Monitor threat detection trends
3. **Health**: Aim for health scores > 75 for optimal performance

### Setting Alerts
1. Navigate to **Settings**
2. Adjust CPU Alert Threshold (default 80%)
3. Adjust Memory Alert Threshold (default 85%)
4. Enable Sound Alerts for critical notifications

---

## ⚙️ Advanced Settings

### Monitoring Interval
**Location**: Settings > Monitoring Interval
- **Default**: 1000ms (1 second)
- **Range**: 500ms to 5000ms
- Faster updates = higher CPU usage
- Slower updates = lower resolution

### Alert Thresholds
**Location**: Settings
- **CPU Threshold**: Default 80% (range 10-95%)
- **Memory Threshold**: Default 85% (range 10-95%)
- Alerts trigger when thresholds exceeded

### Sound Alerts
**Location**: Settings or Profile > Preferences
- Toggle to enable/disable audio notifications
- Notification sound plays for warnings/errors

---

## 🐛 Troubleshooting

### Profile Not Saving
- Check browser localStorage is enabled
- Clear browser cache and try again
- Ensure you clicked "Save" button

### Notifications Not Showing
- Verify notifications are enabled
- Check browser console for errors
- Refresh page to reload notifications

### Charts Not Updating
- Allow 2-3 seconds for initial data collection
- Check metrics API is responding
- Verify WebSocket connection is active

### Sound Not Playing
- Check Profile > Preferences > Notification Sound is enabled
- Verify browser volume is up
- Check system volume settings
- Test with a different browser

---

## 📊 Dashboard Workflow

### Recommended Daily Workflow
1. **Morning**: Check **Reports** > **Health** for system status
2. **Throughout Day**: Monitor **Dashboard** for real-time metrics
3. **When Issues Arise**: Check **Analytics** for trends
4. **End of Day**: Review **Notifications** for any events

### Performance Monitoring
1. View **Dashboard** for current metrics
2. Check **Analytics** for trends
3. Review **Reports** > **Performance** for detailed analysis
4. Use **Alerts** for real-time notifications

### Security Monitoring
1. Run **File Scanner** regularly
2. Review **Alerts** section frequently
3. Check **Reports** > **Security** for scan history
4. Monitor **Notifications** for security events

---

## 🎯 Best Practices

### Profile Management
✅ Keep your profile information updated
✅ Use a strong password (min 6 characters, ideally more)
✅ Enable sound alerts for critical notifications
✅ Set email notifications if available

### Monitoring System
✅ Review analytics regularly to understand patterns
✅ Set appropriate alert thresholds
✅ Keep notification history clean
✅ Monitor system health score

### Data Safety
✅ Profile data auto-saves to localStorage
✅ Clear notifications periodically
✅ Backup important configurations
✅ Document high-priority thresholds

---

## 🔗 API Endpoints (for Developers)

### Profile Endpoints
```
GET  /api/profile/              - Get user profile
PUT  /api/profile/              - Update profile
POST /api/profile/login-update  - Update last login
```

### Notification Endpoints
```
GET    /api/profile/notifications           - Get notifications
POST   /api/profile/notifications           - Create notification
DELETE /api/profile/notifications/{id}     - Delete specific
DELETE /api/profile/notifications          - Clear all
```

---

## 📞 Support & Help

### Common Questions

**Q: How do I reset my profile?**
A: Edit each field in Profile > Personal and click Save.

**Q: Can I export my data?**
A: Profile data is stored in browser localStorage - use browser dev tools to export.

**Q: Will my data be lost if I clear browser cache?**
A: Yes - localStorage data will be cleared. Consider backing it up.

**Q: How are notifications stored?**
A: Notifications are stored in-memory during the session (up to 100).

**Q: Can I change my password?**
A: Yes, in Profile > Security tab.

---

## 🎉 Summary

You now have a **professional, fully-featured monitoring dashboard** with:
- ✅ Complete user profile management
- ✅ Advanced analytics with trend visualization
- ✅ Comprehensive system reports
- ✅ Real-time notifications
- ✅ Customizable preferences
- ✅ Professional, modern UI design

Enjoy using **VigilantAI 2.0**! 🚀

---

**Last Updated**: November 2024
**Version**: 2.0
