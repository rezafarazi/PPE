package com.cyberdyne.rezafta.PPERP.Encriptions;

import com.cyberdyne.rezafta.PPERP.Models.AES_Encription_Model;
import com.cyberdyne.rezafta.PPERP.Models.DES_Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class DESEncription
{

    private static final String ALGORITHM = "DES";

    //Get generate key function start
    private SecretKey GenerateKey() throws Exception
    {
        KeyGenerator keyGen = KeyGenerator.getInstance(ALGORITHM);
        return keyGen.generateKey();
    }
    //Get generate key function end

    //Get encrption function start
    public DES_Encription_Model Encription(String Value) throws Exception
    {
        SecretKey key=GenerateKey();
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedBytes = cipher.doFinal(Value.getBytes());

        return new DES_Encription_Model(
            Base64.getEncoder().encodeToString(encryptedBytes),
            secretKeyToString(key)
        );
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value,String Key) throws Exception
    {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, stringToSecretKey(Key));
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(Value));
        return new String(decryptedBytes);
    }
    //Get decrption function end


    // Method to convert a string to a SecretKey
    private SecretKey stringToSecretKey(String encodedKey)
    {
        byte[] decodedKey = Base64.getDecoder().decode(encodedKey);
        return new SecretKeySpec(decodedKey, 0, decodedKey.length, "DES");
    }

    // Method to convert a SecretKey to a string
    private String secretKeyToString(SecretKey secretKey)
    {
        byte[] encodedKey = secretKey.getEncoded();
        return Base64.getEncoder().encodeToString(encodedKey);
    }

}
