package com.example.project;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class SetConfig extends AppCompatActivity {

    EditText E1,E2,E3;
    Button b1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_config);

        SharedPreferences sh = getSharedPreferences("myPrefs", MODE_PRIVATE);
        String Mobileno1 = sh.getString("Mobileno1", "");
        String Mobileno2 = sh.getString("Mobileno2", "");
        String Mobileno3= sh.getString("Mobileno3", "");


        E1=(EditText)findViewById(R.id.editTextmob1);
        E2=(EditText)findViewById(R.id.editTextmob2);
        E3=(EditText)findViewById(R.id.editTextmob3);

        b1=(Button)findViewById(R.id.buttonsave);

        if(Mobileno1.isEmpty()==false)
        {
            E1.setText(Mobileno1);
        }

        if(Mobileno2.isEmpty()==false)
        {
            E2.setText(Mobileno2);
        }

        if(Mobileno3.isEmpty()==false)
        {
            E3.setText(Mobileno3);
        }

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                SharedPreferences sharedPreferences = getSharedPreferences("myPrefs",MODE_PRIVATE);
                SharedPreferences.Editor myEdit = sharedPreferences.edit();
                myEdit.putString("Mobileno1", E1.getText().toString());
                myEdit.putString("Mobileno2", E2.getText().toString());
                myEdit.putString("Mobileno3", E3.getText().toString());
                myEdit.commit();
            }
        });

    }
}