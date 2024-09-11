package com.cyberdyne.rezafta;

import com.cyberdyne.rezafta.PPERP.Models.RSA_Encription_Model;
import com.cyberdyne.rezafta.PPERP.Models.TimeBase_Encription_Model;
import com.cyberdyne.rezafta.PPERP.PPERP;
import com.cyberdyne.rezafta.PPERP.Requets.Requests;
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
        String s=Requests.StringRequest("https://izino.ir");
        System.out.println(s.toString());
    }
    //Main function end

}
