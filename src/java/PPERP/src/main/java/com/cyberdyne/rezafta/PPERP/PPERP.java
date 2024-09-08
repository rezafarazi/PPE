package com.cyberdyne.rezafta.PPERP;

import com.cyberdyne.rezafta.PPERP.Encriptions.AESEncription;
import com.cyberdyne.rezafta.PPERP.Models.Encription_Model;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

public class PPERP
{

    //Get enciprion function start
    public Encription_Model GetEncription(String value, EncriptionTypes type) throws Exception
    {
        Encription_Model result = null;

        switch (type)
        {
            case AES:
                result = new AESEncription().Encription(value);
                break;
        }

        return result;
    }
    //Get enciprion function end


    //Get decription function start
    public String GetDecription(String value,String key,EncriptionTypes type) throws Exception
    {
        String result="";

        switch (type)
        {
            case AES:
                result = new AESEncription().Decription(value,key);
                break;
        }

        return result;
    }
    //Get decription function end

}
