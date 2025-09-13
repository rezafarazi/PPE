package com.rezafta.PPE;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import com.rezafta.PPE.ParallelProcessing.ParalleDecription;
import com.rezafta.PPE.ParallelProcessing.ParalleEncription;
import com.rezafta.PPE.Types.EncriptionTypes;

import java.util.Base64;
import java.util.concurrent.ForkJoinPool;

public class PPE
{

    //Global variable
    private static AESEncription AES=new AESEncription();

    //Get enciprion function start
    public String GetEncription(String value,String TimeZone,String salt, EncriptionTypes type) throws Exception
    {
        String EnValueA="";
        String EnValueB="";

        //Divied a string to 2 string with string start
        String ValueA=value.substring(0,value.length()/2);
        String ValueB=value.substring(value.length()/2,value.length());
        //Divied a string to 2 string with string end


        //Get prarllel processing start
        ForkJoinPool pool = new ForkJoinPool();

        switch (type)
        {
            case AES:
                ParalleEncription task_aes_left = new ParalleEncription(type,ValueA,TimeZone,salt);
                ParalleEncription task_aes_right = new ParalleEncription(type,ValueB,TimeZone,salt);

                EnValueA = pool.invoke(task_aes_left);
                EnValueB = pool.invoke(task_aes_right);
                break;
            case ChaCha20:
                ParalleEncription task_chacha20_left = new ParalleEncription(type,ValueA,TimeZone,salt);
                ParalleEncription task_chacha20_right = new ParalleEncription(type,ValueB,TimeZone,salt);

                EnValueA = pool.invoke(task_chacha20_left);
                EnValueB = pool.invoke(task_chacha20_right);
                break;
        }

        return Base64.getEncoder().encodeToString((EnValueA+"~|~"+EnValueB).getBytes());
    }
    //Get enciprion function end


    //Get decription function start
    public String GetDecription(String value,String TimeZone,String salt,EncriptionTypes type) throws Exception
    {
        String result="";
        value = new String(Base64.getDecoder().decode(value));

        String ValueA=value.split("~|~")[0];
        String ValueB=value.split("~|~")[1];

        //Thread Pool
        ForkJoinPool pool =new ForkJoinPool();

        switch (type)
        {
            case AES:
                ParalleDecription task_aes_left = new ParalleDecription(type,ValueA,TimeZone,salt);
                ParalleDecription task_aes_right = new ParalleDecription(type,ValueB,TimeZone,salt);

                result += pool.invoke(task_aes_left);
                result += pool.invoke(task_aes_right);

                break;
            case ChaCha20:
                ParalleDecription task_chacha20_left = new ParalleDecription(type,ValueA,TimeZone,salt);
                ParalleDecription task_chacha20_right = new ParalleDecription(type,ValueB,TimeZone,salt);

                result += pool.invoke(task_chacha20_left);
                result += pool.invoke(task_chacha20_right);

                break;
        }

        return result;
    }
    //Get decription function end

}
