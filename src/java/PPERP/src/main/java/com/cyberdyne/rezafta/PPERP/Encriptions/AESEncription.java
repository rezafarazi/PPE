package com.cyberdyne.rezafta.PPERP.Encriptions;

import com.cyberdyne.rezafta.PPERP.Models.Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class AESEncription
{

    //Get generate key function start
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
    //Get generate key function end

    //Get encrption function start
    public Encription_Model Encription(String Value) throws Exception
    {
        String result="";
        String plainText = Value;
        String secretKey = GenerateKey(); // Replace with your own secret key
        //key length to 16, 24, or 32 bytes

        System.out.println(secretKey);

        // Create AES key from the secret key
        SecretKeySpec keySpec = new SecretKeySpec(secretKey.getBytes(), "AES");

        // Initialize the cipher for encryption
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        result = Base64.getEncoder().encodeToString(encryptedBytes);

        return new Encription_Model(result,secretKey);
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value,String Key) throws Exception
    {
        String secretKey = Key; // Replace with your own secret key
        //key length to 16, 24, or 32 bytes

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
