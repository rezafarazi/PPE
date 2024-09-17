package com.cyberdyne.rezafta.PPERP.PPERP;

import com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm.AESEncription;
import com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm.DESEncription;
import com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm.RSAEncription;
import com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm.TimeBaseEncription;
import com.cyberdyne.rezafta.PPERP.PPERP.Types.EncriptionTypes;

public class PPERP
{

    //Global variable
    private static PPERP.Encriptions.Algorithm.RSAEncription RSA=new RSAEncription();
    private static PPERP.Encriptions.Algorithm.AESEncription AES=new AESEncription();
    private static PPERP.Encriptions.Algorithm.DESEncription DES=new DESEncription();
    private static PPERP.Encriptions.Algorithm.TimeBaseEncription TimeBase=new TimeBaseEncription();


    //Get enciprion function start
    public Object GetEncription(String value, PPERP.Types.EncriptionTypes type) throws Exception
    {
        switch (type)
        {
            case AES:
                return AES.Encription(value);
            case RSA:
                return RSA.Encription(value);
            case DES:
                return DES.Encription(value);
            case TIMEBASE:
                return TimeBase.Encription(value);
        }

        throw new Exception("Type not working yet");
    }
    //Get enciprion function end


    //Get decription function start
    public String GetDecription(String value, String key, EncriptionTypes type) throws Exception
    {
        String result="";

        switch (type)
        {
            case AES:
                result = AES.Decription(value,key);
                break;
            case RSA:
                result = RSA.Decription(value);
                break;
            case DES:
                result = DES.Decription(value,key);
                break;
            case TIMEBASE:
                result = TimeBase.Decription(value,key);
                break;
        }

        return result;
    }
    //Get decription function end

}
