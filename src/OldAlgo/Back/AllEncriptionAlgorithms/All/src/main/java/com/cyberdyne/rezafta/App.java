package com.cyberdyne.rezafta;

import com.cyberdyne.rezafta.PPERP.Encriptions.Key.KeyGenerator;
import com.cyberdyne.rezafta.PPERP.Functions.TimeStep.TimeStep;
import com.cyberdyne.rezafta.PPERP.Models.AES_Encription_Model;
import com.cyberdyne.rezafta.PPERP.PPERP;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.sql.Date;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Base64;

public class App
{

    //Main function start
    public static void main( String[] args ) throws Exception
    {

//        String H="Hello world";
//        PPERP p=new PPERP();
//        AES_Encription_Model m = (AES_Encription_Model) p.GetEncription(H, EncriptionTypes.AES);
//
//        String dec = p.GetDecription(m.getValue(),"",EncriptionTypes.AES);
//
//
//        System.out.println("En is "+m.getValue());
//        System.out.println("De is "+dec);

        String plaintext = "Hello world my name is reza"; // The string you want to encrypt
        String secretKey = "JKDBCJKDBBCJKDBJCBKDBCJK"; // Replace with your own secret key

        try
        {
            String enc=ENC(secretKey,plaintext);
            String dec=DEC(secretKey,enc);

            System.out.println("ENC : "+enc);
            System.out.println("DEC : "+dec);

        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

    }
    //Main function end


    public static String ENC(String sec,String val) throws Exception
    {
        byte[] keyBytes = sec.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");

        // Initialize the cipher in ECB mode
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(val.getBytes(StandardCharsets.UTF_8));

        // Encode the encrypted bytes as base64
        String encryptedBase64 = Base64.getEncoder().encodeToString(encryptedBytes);

        return encryptedBase64;
    }

    public static String DEC(String sec,String val) throws Exception
    {
        byte[] keyBytes = sec.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");

        // Initialize the cipher in decryption mode
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);

        // Decode the base64-encoded ciphertext
        byte[] encryptedBytes = Base64.getDecoder().decode(val);

        // Decrypt the ciphertext
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);

        // Convert the decrypted bytes back to a string
        String decryptedText = new String(decryptedBytes, StandardCharsets.UTF_8);

        return decryptedText;
    }


}
