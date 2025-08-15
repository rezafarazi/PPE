package com.rezafta.PPE.Functions.KeyConvertor;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class KeyConvertor
{


    // Method to convert a string to a SecretKey
    public static SecretKey stringToSecretKey(String encodedKey,String algorithm)
    {
        byte[] decodedKey = Base64.getDecoder().decode(encodedKey);
        return new SecretKeySpec(decodedKey, 0, decodedKey.length, algorithm);
    }

    // Method to convert a SecretKey to a string
    public static String secretKeyToString(SecretKey secretKey)
    {
        byte[] encodedKey = secretKey.getEncoded();
        return Base64.getEncoder().encodeToString(encodedKey);
    }


}
