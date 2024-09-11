package com.cyberdyne.rezafta;

import com.cyberdyne.rezafta.PPERP.Models.RSA_Encription_Model;
import com.cyberdyne.rezafta.PPERP.Models.TimeBase_Encription_Model;
import com.cyberdyne.rezafta.PPERP.PPERP;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Base64;

public class App
{

    //Main function start
    public static void main( String[] args ) throws Exception
    {
        for(int i=0;i<10;i++) {
            PPERP pp = new PPERP();

            Object mo = pp.GetEncription("Hello wolrd", EncriptionTypes.TIMEBASE);
            TimeBase_Encription_Model d = (TimeBase_Encription_Model) mo;
            System.out.println(d.getValue());

            String result = pp.GetDecription(d.getValue(), d.getKey(), EncriptionTypes.TIMEBASE);
            System.out.println(result);
        }
    }
    //Main function end

}
