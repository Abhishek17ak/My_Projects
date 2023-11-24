package com.example.project;


import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;

import com.example.project.ui.camera.GraphicOverlay;
import com.google.android.gms.vision.face.Face;
import android.content.SharedPreferences;

class FaceGraphic extends GraphicOverlay.Graphic {
    private static final float FACE_POSITION_RADIUS = 10.0f;
    private static final float ID_TEXT_SIZE = 40.0f;
    private static final float ID_Y_OFFSET = 50.0f;
    private static final float ID_X_OFFSET = -50.0f;
    private static final float BOX_STROKE_WIDTH = 5.0f;


    private Paint mFacePositionPaint;
    private Paint mIdPaint;
    private Paint mBoxPaint;
    Context context;




    private volatile Face mFace;

    FaceGraphic(GraphicOverlay overlay, Context aContext) {
        super(overlay);
        context= aContext;
        mFacePositionPaint = new Paint();
        mFacePositionPaint.setColor(Color.GREEN);

        mIdPaint = new Paint();
        mIdPaint.setColor(Color.RED);
        mIdPaint.setTextSize(ID_TEXT_SIZE);

        mBoxPaint = new Paint();
        mBoxPaint.setColor(Color.BLUE);
        mBoxPaint.setStyle(Paint.Style.STROKE);
        mBoxPaint.setStrokeWidth(BOX_STROKE_WIDTH);
    }

    void setId(int id) {

    }


    /**
     * Updates the face instance from the detection of the most recent frame.  Invalidates the
     * relevant portions of the overlay to trigger a redraw.
     */
    void updateFace(Face face) {
        mFace = face;
        postInvalidate();
    }

    /**
     * Draws the face annotations for position on the supplied canvas.
     */
    @Override
    public void draw(Canvas canvas) {
        Face face = mFace;
        if (face == null) {
            return;
        }

        // Draws a circle at the position of the detected face, with the face's track id below.
        float x = translateX(face.getPosition().x + face.getWidth() / 2);
        float y = translateY(face.getPosition().y + face.getHeight() / 2);
        y=y-(y/100)*30;
        canvas.drawCircle(x, y, FACE_POSITION_RADIUS, mFacePositionPaint);
        canvas.drawText("left eye: " + String.format("%.2f", face.getIsRightEyeOpenProbability()), x + ID_X_OFFSET * 4, y - ID_Y_OFFSET * 2, mIdPaint);
        canvas.drawText("right eye: " + String.format("%.2f", face.getIsLeftEyeOpenProbability()), x - ID_X_OFFSET*2, y - ID_Y_OFFSET*2, mIdPaint);

        SharedPreferences sh = context.getSharedPreferences("MySharedPref", context.MODE_PRIVATE);
        SharedPreferences.Editor myEdit = sh.edit();
        myEdit.putString("RightEye", Integer.toString((int)(face.getIsRightEyeOpenProbability()*100)));
        myEdit.putString("LeftEye", Integer.toString((int)(face.getIsLeftEyeOpenProbability()*100)));
        myEdit.commit();

        // Draws a bounding box around the face.
        float xOffset = scaleX(face.getWidth() / 2.0f);
        float yOffset = scaleY(face.getHeight() / 2.5f);
        float left = x - xOffset;
        float top = y - yOffset;
        float right = x + xOffset;
        float bottom = y + yOffset;
        canvas.drawRect(left, top, right, bottom, mBoxPaint);
    }
}