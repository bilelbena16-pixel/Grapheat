#!/bin/bash
# Construit un APK (WebView) pour un employé : ./build_apk.sh <cle> <Nom> <SDK_DIR> <KEYSTORE>
set -euo pipefail
KEY=$1; NAME=$2; SDK=$3; KS=$4
BT=$SDK/android-15; JAR=$SDK/android-35/android.jar
HERE=$(cd "$(dirname "$0")" && pwd); SRC=$HERE/../$KEY; [ "$KEY" = appartements ] && SRC=$HERE/..
W=$(mktemp -d); PKG=com.bookingalger.$KEY
mkdir -p $W/assets $W/res $W/src/com/bookingalger/$KEY $W/classes $W/dex
cp $SRC/index.html $W/assets/index.html; cp -r $SRC/img $W/assets/img
for d in mdpi:48 hdpi:72 xhdpi:96 xxhdpi:144 xxxhdpi:192; do
  mkdir -p $W/res/mipmap-${d%%:*}
  python3 -c "from PIL import Image; im=Image.open('$SRC/img/icon-512.png'); im.resize((${d##*:},${d##*:}),Image.LANCZOS).save('$W/res/mipmap-${d%%:*}/ic_launcher.png')"
done
cat > $W/AndroidManifest.xml <<XML
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="$PKG">
  <uses-permission android:name="android.permission.INTERNET"/>
  <uses-permission android:name="android.permission.VIBRATE"/>
  <application android:label="BA $NAME" android:icon="@mipmap/ic_launcher" android:allowBackup="true"
      android:theme="@android:style/Theme.Material.Light.NoActionBar">
    <activity android:name=".MainActivity" android:exported="true"
        android:configChanges="orientation|screenSize|keyboardHidden|uiMode" android:windowSoftInputMode="adjustResize">
      <intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
    </activity>
  </application>
</manifest>
XML
cat > $W/src/com/bookingalger/$KEY/MainActivity.java <<JAVA
package $PKG;
import android.app.Activity; import android.content.Intent; import android.graphics.Color; import android.net.Uri;
import android.os.Build; import android.os.Bundle; import android.view.View; import android.view.Window;
import android.webkit.*;
public class MainActivity extends Activity {
  private WebView web;
  @Override protected void onCreate(Bundle state) {
    super.onCreate(state);
    Window w = getWindow(); w.setStatusBarColor(Color.WHITE); w.setNavigationBarColor(Color.WHITE);
    int f = View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR; if (Build.VERSION.SDK_INT >= 26) f |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
    w.getDecorView().setSystemUiVisibility(f);
    web = new WebView(this); web.setBackgroundColor(Color.WHITE);
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setDatabaseEnabled(true); s.setAllowFileAccess(true); s.setTextZoom(100);
    web.setWebViewClient(new WebViewClient() {
      @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
        Uri u = r.getUrl(); if ("file".equals(u.getScheme())) return false;
        try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception e) {} return true; } });
    web.setWebChromeClient(new WebChromeClient());
    setContentView(web);
    if (state != null) web.restoreState(state); else web.loadUrl("file:///android_asset/index.html");
  }
  @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }
  @Override public void onBackPressed() { if (web.canGoBack()) web.goBack(); else super.onBackPressed(); }
}
JAVA
$BT/aapt2 compile --dir $W/res -o $W/res.zip
$BT/aapt2 link -o $W/base.apk -I $JAR --manifest $W/AndroidManifest.xml -A $W/assets \
  --min-sdk-version 24 --target-sdk-version 34 --version-code 1 --version-name 1.0 $W/res.zip
javac -nowarn -source 8 -target 8 -bootclasspath $JAR -d $W/classes $W/src/com/bookingalger/$KEY/MainActivity.java 2>&1 | grep -v "warning" || true
$BT/d8 --release --min-api 24 --lib $JAR --output $W/dex $(find $W/classes -name '*.class')
(cd $W/dex && zip -q -u $W/base.apk classes.dex)
$BT/zipalign -p -f 4 $W/base.apk $W/aligned.apk
$BT/apksigner sign --ks $KS --ks-pass pass:bookingalger --key-pass pass:bookingalger --out $HERE/BookingAlger-$NAME.apk $W/aligned.apk
$BT/apksigner verify --min-sdk-version 24 $HERE/BookingAlger-$NAME.apk && echo "OK $HERE/BookingAlger-$NAME.apk"
rm -rf $W
