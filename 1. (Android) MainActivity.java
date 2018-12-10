
    '''
    Author: Manal Alduraibi
    Last modified: 12/04/2018
    First, we built our application by following this tutorial https://codinginflow.com/tutorials/android/text-to-speech
    and then we add our new features on it and play with the voice rate that we have.
    '''

package com.example.manalalduraibi.myapplication1;


import android.os.Build;
import android.speech.tts.TextToSpeech;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import java.util.Locale;





public class MainActivity extends AppCompatActivity {
    private TextToSpeech mTTS;
    private EditText mEditText;
    private SeekBar mSeekBarPitch;
    private SeekBar mSeekBarSpeed;
    private Button mButtonSpeak;
    private Button mButtonHappy;
    private Button mButtonSad;
    private Button mButtonAngry;
    private String TAG  = "TTS";


    private static String happySymbol = ":)";
    private static String sadSymbol = ":(";
    private static String angrySymbol = ":o";

    private static final float happyPitch = 0.94f;
    private static final float happySpeed = 1.14f;

    private static final float sadPitch = 1.48f;
    private static final float sadSpeed = 0.72f;

    private static final float angryPitch = 0.56f;
    private static final float angrySpeed = 1.52f;

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mButtonSpeak = findViewById(R.id.button_speak);

        mButtonHappy = findViewById(R.id.button_happy);
        mButtonSad = findViewById(R.id.button_sad);
        mButtonAngry = findViewById(R.id.button_angry);

        mTTS = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int result = mTTS.setLanguage(Locale.US);

                    if (result == TextToSpeech.LANG_MISSING_DATA
                            || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e(TAG, "Language not supported");
                    } else {
                        mButtonSpeak.setEnabled(true);
                    }
                } else {
                    Log.e(TAG, "Initialization failed");
                }
            }
        },"com.google.android.tts");



        mEditText = findViewById(R.id.edit_text);
        mSeekBarPitch = findViewById(R.id.seek_bar_pitch);
        mSeekBarSpeed = findViewById(R.id.seek_bar_speed);

        mButtonSpeak.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                speak();
            }
        });

        mButtonHappy.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSeekBarPitch.setProgress((int)(happyPitch*50));
                mSeekBarSpeed.setProgress((int)(happySpeed*50));
            }
        });

        mButtonSad.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSeekBarPitch.setProgress((int)(sadPitch*50));
                mSeekBarSpeed.setProgress((int)(sadSpeed*50));
            }
        });

        mButtonAngry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSeekBarPitch.setProgress((int)(angryPitch*50));
                mSeekBarSpeed.setProgress((int)(angrySpeed*50));
            }
        });

    }

    private void speak() {
        String text = mEditText.getText().toString();


        if(text.contains(happySymbol)){

            text = text.replace(happySymbol,"");


            mButtonHappy.performClick();
        }


        if(text.contains(sadSymbol)){

            text = text.replace(sadSymbol,"");

            mButtonSad.performClick();
        }


        if(text.contains(angrySymbol)){

            text = text.replace(angrySymbol,"");

            mButtonAngry.performClick();
        }




        float pitch = (float) mSeekBarPitch.getProgress() / 50;
        if (pitch < 0.1) pitch = 0.1f;
        float speed = (float) mSeekBarSpeed.getProgress() / 50;
        if (speed < 0.1) speed = 0.1f;

        mTTS.setPitch(pitch);
        mTTS.setSpeechRate(speed);

        mTTS.speak(text, TextToSpeech.QUEUE_FLUSH, null);

        Log.d(TAG, "speak: Current pitch: "+pitch);
        Log.d(TAG, "speak: Current speed: "+speed);
    }

    @Override
    protected void onDestroy() {
        if (mTTS != null) {
            mTTS.stop();
            mTTS.shutdown();
        }

        super.onDestroy();
    }
}
