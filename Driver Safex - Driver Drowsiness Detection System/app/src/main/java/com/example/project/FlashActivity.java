package com.example.project;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;

public class FlashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_flash);

        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }



        SharedPreferences sh = getSharedPreferences("MySharedPref", MODE_PRIVATE );
        //String RightEye = sh.getString("RightEye", "");
        //String LeftEye = sh.getString("LeftEye", "");
        SharedPreferences.Editor myEdit = sh.edit();
        myEdit.putString("RightEye", "");
        myEdit.putString("LeftEye", "");
        myEdit.commit();

        int secondsDelayed = 1;
        new Handler().postDelayed(new Runnable() {
            public void run() {

                // Get SharedPreferences instance
                SharedPreferences preferences = getSharedPreferences("myPrefs", MODE_PRIVATE);

                if (preferences.contains("Mobileno1")) {
                    String value = preferences.getString("Mobileno1", "");
                    startActivity(new Intent(FlashActivity.this, FaceActivity.class));
                    finish();
                } else {
                    startActivity(new Intent(FlashActivity.this, SetConfig.class));
                    finish();
                }


            }
        }, secondsDelayed * 3000);
    }
}