package com.rezafta.PPE;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import com.rezafta.PPE.Models.Encription_Model;
import com.rezafta.PPE.ParallelProcessing.AESParalleDecription;
import com.rezafta.PPE.ParallelProcessing.AESParalleEncription;
import com.rezafta.PPE.Types.EncriptionTypes;

import java.util.ArrayList;
import java.util.Base64;
import java.util.concurrent.ForkJoinPool;

public class PPE
{

    //Global variable
    private static AESEncription AES=new AESEncription();

    //Get enciprion function start
    public String GetEncription(String value,String salt, EncriptionTypes type) throws Exception
    {
        String EnValueA="";
        String EnValueB="";

        //Divied a string to 2 string with string start
        String ValueA=value.substring(0,value.length()/2);
        String ValueB=value.substring(value.length()/2,value.length());
        //Divied a string to 2 string with string end

        switch (type)
        {
            case AES:

                //Get prarllel processing start
                ForkJoinPool pool =new ForkJoinPool();

                AESParalleEncription task_left = new AESParalleEncription(ValueA,salt);
                AESParalleEncription task_right = new AESParalleEncription(ValueB,salt);
//                EnValueA = AES.Encription(ValueA,salt);
//                EnValueB = AES.Encription(ValueB,salt);
                EnValueA = pool.invoke(task_left);
                EnValueB = pool.invoke(task_right);

                //Get prarllel processing end

                break;
        }

        return Base64.getEncoder().encodeToString((EnValueA+"~|~"+EnValueB).getBytes());
    }
    //Get enciprion function end


    //Get decription function start
    public String GetDecription(String value,String salt,EncriptionTypes type) throws Exception
    {
        String result="";
        value = new String(Base64.getDecoder().decode(value));

        String ValueA=value.split("~|~")[0];
        String ValueB=value.split("~|~")[2];

        switch (type)
        {
            case AES:
//                result = AES.Decription(ValueA,salt);
//                result += AES.Decription(ValueB,salt);
                ForkJoinPool pool =new ForkJoinPool();

                AESParalleDecription task_left = new AESParalleDecription(ValueA,salt);
                AESParalleDecription task_right = new AESParalleDecription(ValueB,salt);

                result += pool.invoke(task_left);
                result += pool.invoke(task_right);

                break;
        }

        return result;
    }
    //Get decription function end

}
