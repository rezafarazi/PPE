package com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm;

import com.cyberdyne.rezafta.PPERP.PPERP.Models.TimeBase_Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class TimeBaseEncription {

    //Get generate key function start
    private String GenerateKey(long time) throws Exception
    {
        byte[] keyBytes = new byte[16];
        SecureRandom random = new SecureRandom();
        random.setSeed(time);
        random.nextBytes(keyBytes);

        // Convert the key to a hexadecimal string
        StringBuilder hexString = new StringBuilder();
        for (byte b : keyBytes) {
            hexString.append(String.format("%02X", b));
        }

        return hexString.toString().substring(0,16);
    }
    //Get generate key function end

    //Get encrption function start
    public PPERP.Models.TimeBase_Encription_Model Encription(String Value) throws Exception {
        //Get time
        long currentTime = System.currentTimeMillis();

        String result="";
        String plainText = Value;
        String secretKey = GenerateKey(currentTime); // Replace with your own secret key
        //key length to 16, 24, or 32 bytes

//        System.out.println(secretKey);

        // Create AES key from the secret key
        SecretKeySpec keySpec = new SecretKeySpec(secretKey.getBytes(), "AES");

        // Initialize the cipher for encryption
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        result = Base64.getEncoder().encodeToString(encryptedBytes);

        return new TimeBase_Encription_Model(result,secretKey);
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value, String Key) throws Exception
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

