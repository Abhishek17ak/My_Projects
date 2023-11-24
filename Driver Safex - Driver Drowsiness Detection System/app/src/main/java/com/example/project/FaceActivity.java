package com.example.project;


import androidx.appcompat.app.AppCompatActivity;
import android.app.Dialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.StrictMode;
import android.telephony.SmsManager;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import com.example.project.ui.camera.CameraSourcePreview;
import com.example.project.ui.camera.GraphicOverlay;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.MultiProcessor;
import com.google.android.gms.vision.Tracker;
import com.google.android.gms.vision.face.Face;
import com.google.android.gms.vision.face.FaceDetector;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

public class FaceActivity extends AppCompatActivity {

    private CameraSource mCameraSource = null;

    private CameraSourcePreview mPreview;
    private GraphicOverlay mGraphicOverlay;

    private static final int RC_HANDLE_GMS = 9001;

    Timer timer;
    MyTimerTask myTimerTask;
    GPSTracker gps;

    int ac=0;
    int SMSsend=0;
    String Mobileno1="";
    String Mobileno2="";
    String Mobileno3="";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_face);

        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        mPreview = (CameraSourcePreview) findViewById(R.id.preview);
        mGraphicOverlay = (GraphicOverlay) findViewById(R.id.faceOverlay);



        FloatingActionButton fab=(FloatingActionButton)findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(FaceActivity.this, SetConfig.class));
            }
        });

        FloatingActionButton fab1=(FloatingActionButton)findViewById(R.id.fab1);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
                finishAffinity();
                System.exit(0);
            }
        });

        createCameraSource();


        timer = new Timer();
        myTimerTask = new MyTimerTask();
        timer.schedule(myTimerTask, 1000, 1000);

    }



    class MyTimerTask extends TimerTask {

        @Override
        public void run() {

            runOnUiThread(new Runnable(){

                @Override
                public void run() {
                    getlocval();

                }});
        }

    }


    public void getlocval()
    {
        SharedPreferences sh = getSharedPreferences("MySharedPref", MODE_PRIVATE);
        String RightEye = sh.getString("RightEye", "");
        String LeftEye = sh.getString("LeftEye", "");

        /*
        int cc=globalVariable.getRCountval()+globalVariable.getLCountval();
        String cc1  = Integer.toString(globalVariable.getRCountval()+globalVariable.getLCountval());
        if(cc<=60 && cc>=4)
        {
            ac++;
        }
        else{
            ac=0;
        }
        */
        //Toast.makeText(getApplicationContext(), RightEye+"-"+LeftEye, Toast.LENGTH_SHORT).show();
        if(RightEye.equals("")) {
            RightEye="0";
            ac=0;
            SMSsend=0;
        }
        if(LeftEye.equals("")) {
            LeftEye="0";
            ac=0;
            SMSsend=0;
        }
        int cc=Integer.parseInt(RightEye);
        int cc1=Integer.parseInt(LeftEye);
        //if(cc<=25 && cc>=4 && cc1<=25 && cc1>=4)
        if(cc<=15 && cc1<=15)
        {
            ac++;
        }
        else{
            ac=0;
            SMSsend=0;
        }

        if(ac>=3) {
            ///Toast.makeText(getApplicationContext(), "Driver Sleep Detect"+cc1, Toast.LENGTH_SHORT).show();
            gps = new GPSTracker(this);

            if (gps.canGetLocation()) {

                double latitude = gps.getLatitude();
                double longitude = gps.getLongitude();
                Toast.makeText(getApplicationContext(), "Your Location is - \nLat: " + latitude + "\nLong: " + longitude, Toast.LENGTH_LONG).show();

                String SMSval = "Family member in trouble http://maps.google.com/maps?q=" + Double.toString(latitude) + "," + Double.toString(longitude);
                if(SMSsend==0)
                {
                    SharedPreferences sh1 = getSharedPreferences("myPrefs", MODE_PRIVATE);
                    Mobileno1 = sh1.getString("Mobileno1", "");
                    Mobileno2 = sh1.getString("Mobileno2", "");
                    Mobileno3 = sh1.getString("Mobileno3", "");

                    onSend(Mobileno1, SMSval);
                    onSend(Mobileno2, SMSval);
                    onSend(Mobileno3, SMSval);
                    SMSsend=1;
                    Toast.makeText(getApplicationContext(), Mobileno1+','+Mobileno2+','+Mobileno3+'-'+SMSval, Toast.LENGTH_LONG).show();

                    // Load the beep sound file
                    MediaPlayer mediaPlayer = MediaPlayer.create(this, R.raw.emergency);

                    // Play the beep sound
                    mediaPlayer.start();

                    // Release the MediaPlayer resources after the sound finishes playing
                    mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                        @Override
                        public void onCompletion(MediaPlayer mediaPlayer) {
                            mediaPlayer.release();
                        }
                    });
                }

            } else {

                gps.showSettingsAlert();
            }
        }
    }


    private void createCameraSource() {

        FaceDetector detector = new FaceDetector.Builder(this)
                .setClassificationType(FaceDetector.ALL_CLASSIFICATIONS)
                .build();

        detector.setProcessor(
                new MultiProcessor.Builder<>(new GraphicFaceTrackerFactory())
                        .build());



        mCameraSource = new CameraSource.Builder(this, detector)
                .setRequestedPreviewSize(640, 480)
                .setFacing(CameraSource.CAMERA_FACING_FRONT)
                .setRequestedFps(30.0f)
                .build();
    }

    /**
     * Restarts the camera.
     */
    @Override
    protected void onResume() {
        super.onResume();

        startCameraSource();
    }

    /**
     * Stops the camera.
     */
    @Override
    protected void onPause() {
        super.onPause();
        mPreview.stop();
    }

    /**
     * Releases the resources associated with the camera source, the associated detector, and the
     * rest of the processing pipeline.
     */
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mCameraSource != null) {
            mCameraSource.release();
        }
    }




    private void startCameraSource() {

        // check that the device has play services available.
        int code = GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(
                getApplicationContext());
        if (code != ConnectionResult.SUCCESS) {
            Dialog dlg =
                    GoogleApiAvailability.getInstance().getErrorDialog(this, code, RC_HANDLE_GMS);
            dlg.show();
        }

        if (mCameraSource != null) {
            try {
                mPreview.start(mCameraSource, mGraphicOverlay);
            } catch (IOException e) {
                 mCameraSource.release();
                mCameraSource = null;
            }
        }
    }


    private class GraphicFaceTrackerFactory implements MultiProcessor.Factory<Face> {
        @Override
        public Tracker<Face> create(Face face) {
            return new GraphicFaceTracker(mGraphicOverlay);
        }
    }


    private class GraphicFaceTracker extends Tracker<Face> {
        private GraphicOverlay mOverlay;
        private FaceGraphic mFaceGraphic;

        GraphicFaceTracker(GraphicOverlay overlay) {
            mOverlay = overlay;
            mFaceGraphic = new FaceGraphic(overlay,getApplicationContext());
        }

        /**
         * Start tracking the detected face instance within the face overlay.
         */
        @Override
        public void onNewItem(int faceId, Face item) {
            mFaceGraphic.setId(faceId);
        }

        /**
         * Update the position/characteristics of the face within the overlay.
         */
        @Override
        public void onUpdate(FaceDetector.Detections<Face> detectionResults, Face face) {
            mOverlay.add(mFaceGraphic);
            mFaceGraphic.updateFace(face);
        }

        /**
         * Hide the graphic when the corresponding face was not detected.  This can happen for
         * intermediate frames temporarily (e.g., if the face was momentarily blocked from
         * view).
         */
        @Override
        public void onMissing(FaceDetector.Detections<Face> detectionResults) {
            mOverlay.remove(mFaceGraphic);
        }

        /**
         * Called when the face is assumed to be gone for good. Remove the graphic annotation from
         * the overlay.
         */
        @Override
        public void onDone() {
            mOverlay.remove(mFaceGraphic);
        }
    }

    public void onSend(String phoneNumber, String smsBody) {

        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phoneNumber, null, smsBody, null, null);
            Toast.makeText(getApplication(), "Send..." ,Toast.LENGTH_LONG).show();

        } catch (Exception e) {
            Toast.makeText(getApplicationContext(),
                    "SMS faild, please try again later!",
                    Toast.LENGTH_LONG).show();
            e.printStackTrace();
        }

    }
}