# <img src="/static/appIcon.png" width="30"/> Niksms Alert Action for Splunk 📢
![GitHub release (latest by date)](https://img.shields.io/badge/Version-v1.2.2-blue)  ![Python 3](https://img.shields.io/badge/Python-3-blue)  

---

## 📌 Overview  
This is a **Splunk Custom Alert Action** for sending SMS messages to a group of phone numbers using the **Niksms API**.  

The App is fully **Python 3 compatible** and supports **Splunk 8+**.  

All activities, including API requests, responses, and errors, are logged to:  

$SPLUNK_HOME/var/log/splunk/niksms_alert.log

---

## 🚀 Features  
- Send Splunk alerts directly to Niksms recipients.  
- Supports **Result Tokens** such as:  
`$result.fieldname$`
- Logging for troubleshooting: `niksms_alert.log`.  

---

## ⚙️ Installation  
1. Download the app package.  
2. In Splunk Web:  
 **Manage Apps → Install app from file**  
3. Upload the app package.  
4. Configure the app in **Manage Apps → Alert Actions**.  

---

## 🔑 Configuration  
1. Sign up on [Niksms](https://niksms.com/) and obtain your **API Key**.  
2. Configure the custom alert action in Splunk with the following parameters:  
 - **API Key** → Your Niksms API key  
 - **Sender Number** → Optional sender number  
 - **Phones** → Comma-separated recipient phone numbers  
 - **Message** → Message text (supports result tokens)  

---

## 🐞 Troubleshooting  
Check logs in:  
- `$SPLUNK_HOME/var/log/splunk/niksms_alert.log`  

If sending fails, verify:  
- Panel have enough charge
- API key is correct and configure correctly
- Phone numbers are valid
- for other errors, check niksms panel logs
    

---

## 🔒 Recommended Permissions  
| Item                         | Permission |
|-------------------------------|------------|
| App Directory                 | 755        |
| Files inside the App          | 644        |
| Executable Scripts in `bin/` | 755        |

---

## 📄 License & Support  
This App is built and maintained under **MIT License**.  
For issues, open a ticket in [GitHub Issues](../../issues).  

