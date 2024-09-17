package com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm;

import com.cyberdyne.rezafta.PPERP.PPERP.Functions.KeyConvertor.KeyConvertor;
import com.cyberdyne.rezafta.PPERP.PPERP.Models.DES_Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
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
    public PPERP.Models.DES_Encription_Model Encription(String Value) throws Exception
    {
        SecretKey key=GenerateKey();
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedBytes = cipher.doFinal(Value.getBytes());

        return new DES_Encription_Model(
            Base64.getEncoder().encodeToString(encryptedBytes),
            PPERP.Functions.KeyConvertor.KeyConvertor.secretKeyToString(key)
        );
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value,String Key) throws Exception
    {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, KeyConvertor.stringToSecretKey(Key,"DES"));
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(Value));
        return new String(decryptedBytes);
    }
    //Get decrption function end

}
