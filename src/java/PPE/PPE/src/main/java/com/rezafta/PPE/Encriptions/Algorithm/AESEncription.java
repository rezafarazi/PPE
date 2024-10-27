package com.rezafta.PPE.Encriptions.Algorithm;

import com.rezafta.PPE.Models.Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
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
    public String Encription(String Value,String Salt) throws Exception
    {
        //Get generate key by timestep
        String secretKey = new String(com.rezafta.PPE.Encriptions.Key.KeyGenerator.GetCurrentTimeKey(Salt).getBytes());
        secretKey=secretKey.substring(0,16);

        byte[] keyBytes = secretKey.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");

        // Initialize the cipher in ECB mode
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(Value.getBytes(StandardCharsets.UTF_8));

        // Encode the encrypted bytes as base64
        String encryptedBase64 = Base64.getEncoder().encodeToString(encryptedBytes);

        return encryptedBase64;
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value,String Slat) throws Exception
    {
        String secretKey = new String(com.rezafta.PPE.Encriptions.Key.KeyGenerator.GetCurrentTimeKey(Slat).getBytes());
        secretKey=secretKey.substring(0,16);

//        // Create AES key from the secret key
//        SecretKeySpec keySpec = new SecretKeySpec(secretKey.getBytes(), "AES");
//
//        // Initialize the cipher for encryption
//        Cipher cipher = Cipher.getInstance("AES");
//        cipher.init(Cipher.DECRYPT_MODE, keySpec);
//
//        // Decrypt the ciphertext
//        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(Value));
//        String decryptedText = new String(decryptedBytes);

        byte[] keyBytes = secretKey.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");

        // Initialize the cipher in decryption mode
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);

        // Decode the base64-encoded ciphertext
        byte[] encryptedBytes = Base64.getDecoder().decode(Value);

        // Decrypt the ciphertext
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);

        // Convert the decrypted bytes back to a string
        String decryptedText = new String(decryptedBytes, StandardCharsets.UTF_8);

        return decryptedText;
    }
    //Get decrption function end

}
