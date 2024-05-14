
```
/Users/josh/Downloads/stsw-link007/AllPlatforms
% find . | xargs xattr -d com.apple.quarantine
% codesign -s - native/mac_x64/libSTLinkUSBDriver.dylib
% codesign -s - native/mac_x64/libusb-1.0.0.dylib
% /Applications/STM32CubeMX.app/Contents/Resources/jre/Contents/Home/bin/java -jar STLinkUpgrade.jar
```

