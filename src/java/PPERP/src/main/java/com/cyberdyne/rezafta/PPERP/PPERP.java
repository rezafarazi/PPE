package com.cyberdyne.rezafta.PPERP;

import com.cyberdyne.rezafta.PPERP.Encriptions.AESEncription;
import com.cyberdyne.rezafta.PPERP.Encriptions.DESEncription;
import com.cyberdyne.rezafta.PPERP.Encriptions.RSAEncription;
import com.cyberdyne.rezafta.PPERP.Models.AES_Encription_Model;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

public class PPERP
{

    //Global variable
    private static RSAEncription RSA=new RSAEncription();
    private static AESEncription AES=new AESEncription();
    private static DESEncription DES=new DESEncription();


    //Get enciprion function start
    public Object GetEncription(String value, EncriptionTypes type) throws Exception
    {
        switch (type)
        {
            case AES:
                return AES.Encription(value);
            case RSA:
                return RSA.Encription(value);
            case DES:
                return DES.Encription(value);
        }

        throw new Exception("Type not working yet");
    }
    //Get enciprion function end


    //Get decription function start
    public String GetDecription(String value,String key,EncriptionTypes type) throws Exception
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
        }

        return result;
    }
    //Get decription function end

}
