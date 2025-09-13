package com.rezafta.PPE.Encriptions.Algorithm;

import com.rezafta.PPE.Encriptions.Concept.IEncription;
import com.rezafta.PPE.Models.Encription_Model;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.ChaCha20ParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Base64;

public class ChaCha20Encryption implements IEncription
{
    private static final int NONCE_SIZE = 12; // ChaCha20 uses 96-bit (12-byte) nonce

    //Get default generate key function start
    public String GenerateKey() throws Exception
    {
        KeyGenerator keyGen = KeyGenerator.getInstance("ChaCha20");
        keyGen.init(256, SecureRandom.getInstanceStrong()); // ChaCha20 uses 256-bit keys
        SecretKey chachaKey = keyGen.generateKey();

        // Convert the key to a hexadecimal string
        byte[] keyBytes = chachaKey.getEncoded();
        StringBuilder hexString = new StringBuilder();
        for (byte b : keyBytes) {
            hexString.append(String.format("%02X", b));
        }

        return hexString.toString().substring(0, 64); // 256 bits = 64 hex characters
    }

    @Override
    public String Encription(String Value, String TimeZone, String Salt) throws Exception {

        // Get generate key by timestep
        String secretKey = new String(com.rezafta.PPE.Encriptions.Key.KeyGenerator.GetCurrentTimeKey(TimeZone, Salt).getBytes());

        // ChaCha20 requires 32-byte (256-bit) key
        byte[] keyBytes = new byte[32];
        byte[] sourceKeyBytes = secretKey.getBytes(StandardCharsets.UTF_8);

        // Pad or truncate to 32 bytes
        if (sourceKeyBytes.length >= 32) {
            System.arraycopy(sourceKeyBytes, 0, keyBytes, 0, 32);
        } else {
            System.arraycopy(sourceKeyBytes, 0, keyBytes, 0, sourceKeyBytes.length);
            // Fill remaining bytes with repeated pattern from source key
            for (int i = sourceKeyBytes.length; i < 32; i++) {
                keyBytes[i] = sourceKeyBytes[i % sourceKeyBytes.length];
            }
        }

        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "ChaCha20");

        // Generate random nonce for ChaCha20
        byte[] nonce = new byte[NONCE_SIZE];
        SecureRandom.getInstanceStrong().nextBytes(nonce);

        ChaCha20ParameterSpec paramSpec = new ChaCha20ParameterSpec(nonce, 1); // counter starts at 1

        // Initialize the cipher
        Cipher cipher = Cipher.getInstance("ChaCha20");
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec, paramSpec);

        // Encrypt the plaintext
        byte[] encryptedBytes = cipher.doFinal(Value.getBytes(StandardCharsets.UTF_8));

        // Combine nonce and encrypted data
        byte[] result = new byte[NONCE_SIZE + encryptedBytes.length];
        System.arraycopy(nonce, 0, result, 0, NONCE_SIZE);
        System.arraycopy(encryptedBytes, 0, result, NONCE_SIZE, encryptedBytes.length);

        // Encode as base64
        String encryptedBase64 = Base64.getEncoder().encodeToString(result);

        return encryptedBase64;
    }

    @Override
    public String Decription(String Value, String TimeZone, String Salt) throws Exception
    {
        String secretKey = new String(com.rezafta.PPE.Encriptions.Key.KeyGenerator.GetCurrentTimeKey(TimeZone, Salt).getBytes());

        // ChaCha20 requires 32-byte (256-bit) key
        byte[] keyBytes = new byte[32];
        byte[] sourceKeyBytes = secretKey.getBytes(StandardCharsets.UTF_8);

        // Pad or truncate to 32 bytes
        if (sourceKeyBytes.length >= 32) {
            System.arraycopy(sourceKeyBytes, 0, keyBytes, 0, 32);
        } else {
            System.arraycopy(sourceKeyBytes, 0, keyBytes, 0, sourceKeyBytes.length);
            // Fill remaining bytes with repeated pattern from source key
            for (int i = sourceKeyBytes.length; i < 32; i++) {
                keyBytes[i] = sourceKeyBytes[i % sourceKeyBytes.length];
            }
        }

        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "ChaCha20");

        // Decode the base64-encoded data
        byte[] encryptedData = Base64.getDecoder().decode(Value);

        // Extract nonce (first 12 bytes) and ciphertext
        if (encryptedData.length < NONCE_SIZE) {
            throw new IllegalArgumentException("Invalid encrypted data: too short");
        }

        byte[] nonce = new byte[NONCE_SIZE];
        byte[] ciphertext = new byte[encryptedData.length - NONCE_SIZE];

        System.arraycopy(encryptedData, 0, nonce, 0, NONCE_SIZE);
        System.arraycopy(encryptedData, NONCE_SIZE, ciphertext, 0, ciphertext.length);

        ChaCha20ParameterSpec paramSpec = new ChaCha20ParameterSpec(nonce, 1); // counter starts at 1

        // Initialize the cipher for decryption
        Cipher cipher = Cipher.getInstance("ChaCha20");
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec, paramSpec);

        // Decrypt the ciphertext
        byte[] decryptedBytes = cipher.doFinal(ciphertext);

        // Convert the decrypted bytes back to a string
        String decryptedText = new String(decryptedBytes, StandardCharsets.UTF_8);

        return decryptedText;
    }
    //Get default generate key function end

}