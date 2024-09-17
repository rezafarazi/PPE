package com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Algorithm;

import com.cyberdyne.rezafta.PPERP.PPERP.Models.RSA_Encription_Model;

import javax.crypto.Cipher;
import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Base64;

public class RSAEncription
{

    // Global variables
    private static final String RSA_ALGORITHM = "RSA";
    private static KeyPair keyPair;


    //Constrator function start
    public RSAEncription()
    {
        try
        {
            GenerateKey();
        }
        catch (Exception e)
        {
            System.out.println("Error RSA Genertion key : "+e.getMessage());
        }
    }
    //Constrator function end

    //Get generate key function start
    private String GenerateKey() throws Exception
    {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance(RSA_ALGORITHM);
        keyGen.initialize(2048); // Key size (in bits)
        keyPair = keyGen.generateKeyPair();

        PublicKey key = keyPair.getPublic();
        byte[] publicbytes = key.getEncoded();

        return Base64.getEncoder().encodeToString(publicbytes);
    }
    //Get generate key function end

    //Get encrption function start
    public PPERP.Models.RSA_Encription_Model Encription(String Value) throws Exception
    {
        // Get the public key from the KeyPair
        PublicKey publicKey = keyPair.getPublic();

        byte[] publicbytes = publicKey.getEncoded();
        String Key = Base64.getEncoder().encodeToString(publicbytes);

        // Initialize a Cipher for encryption
        Cipher cipher = Cipher.getInstance(RSA_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);

        // Encrypt the data
        byte[] encryptedBytes = cipher.doFinal(Value.getBytes());
        return new RSA_Encription_Model(Base64.getEncoder().encodeToString(encryptedBytes),Key);
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value) throws Exception
    {
        // Get the private key from the KeyPair
        PrivateKey privateKey = keyPair.getPrivate();

        // Decode the Base64-encoded encrypted data
        byte[] encryptedBytes = Base64.getDecoder().decode(Value);

        // Initialize a Cipher for decryption with the correct padding scheme
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);

        // Decrypt the data
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
    //Get decrption function end

}
