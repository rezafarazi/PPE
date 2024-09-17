package com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm;

import com.cyberdyne.rezafta.PPERP.PPERP.Models.AES_Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class AESEncription
{

    //Get default generate key function start
    private String GenerateKey() throws Exception
    {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(128, SecureRandom.getInstanceStrong());
        SecretKey aesKey = keyGen.generateKey();

        // Convert the key to a hexadecimal string
        byte[] keyBytes = aesKey.getEncoded();
        StringBuilder hexString = new StringBuilder();
        for (byte b : keyBytes) {
            hexString.append(String.format("%02X", b));
        }

        return hexString.toString().substring(0,16);
    }
    //Get default generate key function end

    //Get encrption function start
    public PPERP.Models.AES_Encription_Model Encription(String Value) throws Exception
    {
        String result="";
        String plainText = Value;


        //Get genearte key by default method
        String secretKey = GenerateKey();

        //Get generate key by timestep
//        String secretKey = new String(Base64.getDecoder().decode(com.cyberdyne.rezafta.PPERP.Encriptions.Key.KeyGenerator.GetCurrentTimeKey("GMT+03:30").getBytes()));

        // Create AES key from the secret key
        SecretKeySpec keySpec = new SecretKeySpec(secretKey.getBytes(), "AES");

        // Initialize the cipher for encryption
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        result = Base64.getEncoder().encodeToString(encryptedBytes);

        return new AES_Encription_Model(result,secretKey);
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value,String Key) throws Exception
    {
        String secretKey = Key;
        //String secretKey = new String(Base64.getDecoder().decode(com.cyberdyne.rezafta.PPERP.Encriptions.Key.KeyGenerator.GetCurrentTimeKey("GMT+03:30").getBytes()));

        // Create AES key from the secret key
        SecretKeySpec keySpec = new SecretKeySpec(secretKey.getBytes(), "AES");

        // Initialize the cipher for encryption
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);

        // Decrypt the ciphertext
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(Value));
        String decryptedText = new String(decryptedBytes);

        return decryptedText;
    }
    //Get decrption function end

}
