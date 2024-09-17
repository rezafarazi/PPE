package com.rezafta.PPE;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import com.rezafta.PPE.Models.Encription_Model;
import com.rezafta.PPE.Types.EncriptionTypes;

import java.util.ArrayList;
import java.util.Base64;

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
                EnValueA = AES.Encription(ValueA,salt);
                EnValueB = AES.Encription(ValueB,salt);
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
                result = AES.Decription(ValueA,salt);
                result += AES.Decription(ValueB,salt);
                break;
        }

        return result;
    }
    //Get decription function end

}
