# Zee's Fabulous Device Farm Notes

This is just a collection of my research and concerns with building our own solution to replace the automation aspect of Kobiton.

## **TL;DR**

I do not think we will be able to build a complete, robuts, and adaptable solution to replace Kobiton in a week. Building a solution specific to Android devices is doable in a few days, and building one for iOS might take a week (and a half); but IMO, building a solution that supports both platforms and won't break at the slightest issue would take a **[‘hot minute’](https://www.urbandictionary.com/define.php?term=hot%20minute)**. 

I am more than happy to work on this solution, but I do not think it can all be done in a week.

## General

### Language

The time limit of this project makes me weary of trying to create a solution in Java. I'm not great with Java and this service needs to be as robust as possible. I would like to implement this using Python because:
<ol type="a">
    <li>I am much more proficient with Python and can build things much quicker; and</li>
    <li>there are quite a few Python libraries for device interaction that could help this project get done faster (I haven't been able to find equivalents for Java).</li>
</ol>


I think building this with Python would be acceptable because once the solution is complete it should require no maintenence in the short term, and minimal maintenence in the long term. It's more important for the actual automated test scripts to be in Java, because Pankaj will need to update those much more frequently.

### Desired Capabilities

If we don't want to keep IPA and APK files in the testing directory, we will need to set up some sort of local service to host application files for Appiums desired capabilities. Installing IPAs may be [more difficult](https://appium.io/docs/en/writing-running-appium/ios/ios-xctest-mobile-apps-management/index.html#mobile-installapp)

### Screen Recording

Currently we link a Kobiton session to the report generated after the tests have been completed. Kobiton records the device screen for the duration of the test and this is helpful when the failure screenshot can't properly show what went wrong. 

Appium does support [screen recording](https://appium.io/docs/en/commands/device/recording-screen/start-recording-screen/), however we would need a place to store the recordings, and a way to link them to the report. With 5 parallel tests each capturing screen recordings, we would be generating a lot of videos. It may be worthwhile to upload them to a GCP storage bucket.

## iOS

Let's get the harder stuff out of the way first. Doing anything with iOS is always challenging because of Apple's walled-garden paradigm. There are a few key components we need to get working in order to run automated tests on iOS with our own device farm:

### Xcode Versions:

In order to support the latest versions of iOS, we would need to constantly be updating our Xcode version (which is usually a 20 - 40 GB download). We may be able to automate this by fetching the latest Xcode version from Apple's servers, but newer Xcode versions do not support older iOS versions. I think we would probably end up with two installed versions of Xcode, one for compatibility with older iOS versions, and the most recent version that is updated often.

In order to use the command line tools that Apple provides for both versions of Xcode, we would likely have to use the `xcode-select` command [to switch between versions](https://hacknicity.medium.com/working-with-multiple-versions-of-xcode-e331c01aa6bc) every time we want to do something with a different version.

### WebDriverAgent: 
Any kind of web view that exists within iOS is [required to use Apple's WebKit](https://www.howtogeek.com/184283/why-third-party-browsers-will-always-be-inferior-to-safari-on-iphone-and-ipad/)  (if you don't use WebKit, your app isn't allowed within 50 ft of the AppStore). This also extends to other browsers that you can download on the AppStore (the iOS versions of Chrome, Brave, Firefox, Opera, Edge, and any other browsers that render on device use WebKit, **not** a mobile version of their desktop engines).

The SmartAccess mobile application uses a WKWebView to render the web content, which is under WebKit; thus, using any kind of 'chromedriver' **would not work**. We need to use a web driver specifically for iOS. Facebook has an [open source webdriver](https://github.com/facebookarchive/WebDriverAgent) which we can use, but it is no longer maintained might take a while to figure out how to build it for the newer versions of iOS.

### Accessing Connected Devices:

Xcode provides a helpful command line tool we can use to list all of the connected iOS devices; however, it also lists all other Apple devices connected to the mac, all simulators Xcode has set up, along with some unnecessary information. The output of the `xcrun xctrace list devices` command [needs to be parsed](https://stackoverflow.com/questions/66041885/how-can-i-get-devices-from-xcrun-xctrace-list-devices-using-python) to get the names and versions of **only** physical devices, because it returns output that looks something like this:

```bash
== Devices ==
Zeeshan’s MacBook Pro (NOT-MY-REAL-UDID)
Zeeshan’s iPhone X (15.0) (ALSO-NOT-MY-REAL-UDID)
Zeeshan’s iPad (6th generation) (14.6) (STILL-NOT-MY-REAL-UDID)

== Simulators ==
Apple TV (14.5) (E98E750F-D39E-4DA0-BB74-E8A5781F372D)
Apple TV 4K (14.5) (55A1FBE8-9C43-41CC-ABF6-F89D397E8785)
Apple TV 4K (2nd generation) (14.5) (449E00D7-4C2B-44DC-B16F-F5D5F15835AD)
Apple TV 4K (at 1080p) (14.5) (CD3CF9C5-8D98-42F0-BDA4-8232BB06A0E4)
Apple TV 4K (at 1080p) (2nd generation) (14.5) (E0A0B3C2-0E54-4E9C-B87E-616B47BC21D8)
iPad (8th generation) (14.5) (A370A6D0-F889-4586-BE79-EFC6B2746879)
iPad Air (4th generation) (14.5) (0A7DEB21-C23D-43CE-BC9E-60F6CC36664E)
...
iPhone 12 mini (14.5) (E99479E9-CADD-4971-A5BF-2929333BE863)
iPhone 12 mini (14.5) + Apple Watch Series 5 - 40mm (7.4) (65DA9770-0A46-42D8-BD46-4D20FB268796)
iPhone 8 (14.5) (F5A4D90F-EF72-487C-A0E6-2474ABC0402D)
iPhone 8 Plus (14.5) (628A0C11-9DF2-472A-A496-BB92008028D2)
iPhone SE (2nd generation) (14.5) (90843E4C-BEB7-4AA2-B007-CC97760AB376)
iPod touch (7th generation) (14.5) (0842FF09-96F5-4D99-8691-E4877C34CCE1)
```

### Installing Apps:

We will need to install SmartAccess app from the IPA file. To automate this, we can use the `ideviceinstaller -i myapp.ipa` command from `libimobiledevice`. In order for this to work, the IPA file must already be [valid and signed](https://stackoverflow.com/a/14652288) or it will not be installed.

### Signing and Certificates:

To build and install the WebDriverAgent on a connected device, we would probably need access to a paid Apple Developer account. We may be able to just build the WebDriverAgent IPA once, have it signed with the account, and use `libimobiledevice` to install the WebDriverAgent alongside the SmartAccess app. Currently with Kobiton, we are using my (Zee) personal developer account which is fine for prototyping but I would like to move away from that in the long term.

## Android

Thankfully, Android devices are going to be less of a hassle. The only major issue we have with automating Android devices is mismatched/unsupported ChromeDriver versions.

### Appium Auto ChromeDriver

Appium has the ability to [automatically detect the Chrome version](http://appium.io/docs/en/writing-running-appium/web/chromedriver/#automatic-discovery-of-compatible-chromedriver) on an Android device, and download the correct ChromeDriver from Chromium servers. Unfortunately for us, Appium can only do this up until Chrome v87.0, and some of our devices use Chrome v90.0+

One possible solution to this would be to use `adb -s <UDID> dumpsys package com.android.chrome | grep versionName` to get the version name of a device, and then download the necessary ChromeDriver from Chromium servers. The [`pure-python-adb`](https://pypi.org/project/pure-python-adb/) library seems like a great way to have this process automated, and then potentially spin up multiple Appium servers with the necessary ChromeDriver. 

With this approach, an issue arises when trying to coordinate which devices need to be connected to which Appium servers. Every new Appium instance will have a different port, and we would most likely need some configuration files to be able to determine which device should be connected to which server. This is a rather inconvenient drawback of this approach as this config file would need to be updated quite often. A possible YAML config file might look like this:

```yaml
android:
    - name: Zebra ET51
      port: 4732
      chromeVersion: 90.0
    - name: Galaxy Tab Active2
      port: 4733
      chromeVersion: 87.0
ios:
    - name: iPhone X
      port: 4734
    - name: iPad Pro
      port: 4735
```

Another possible solution would be to downgrade all devices with Chrome > v87.0 down to v87.0, and use Appiums auto ChromeDriver capability. This would mimick what Kobiton does, and probably work much better than the above soluton. From my experimentation, I have not been able to [downgrade Chrome via ADB](https://www.xda-developers.com/downgrade-an-app-android-no-root/), but I'm pretty sure we would be able to figure that out. I think it might go something like this:

```python
from ppadb.client import Client as AdbClient

apk_path = "pat/to/chrome_v87.0.apk"
identifier = "com.android.chrome"

# 127.0.0.1:5037 is the default
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

for device in devices:
    cmd = f"dumpsys package {identifier} | grep versionName"
    chrome_ver = device.shell(cmd).strip().split("=")[-1].split('.')[0]

    if int(chrome_ver) > 87:
        device.push(apk_path, "/sdcard/chrome.apk")
        device.shell("pm install -d /sdcard/chrome.apk")
```

### Accessing Devices Remotely (with debugging):

I came accross this open source [device farm management tool](https://github.com/DeviceFarmer/stf), which claims to support Chrome remote debugging for Android devices. This could be a potential alternative to GigaFox (although it is Android exclusive).