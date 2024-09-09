package com.cyberdyne.rezafta.PPERP.Encriptions;

import com.cyberdyne.rezafta.PPERP.Models.ECC_Encription_Model;
import com.cyberdyne.rezafta.PPERP.Models.RSA_Encription_Model;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.jce.spec.IESParameterSpec;

import javax.crypto.Cipher;
import java.security.*;
import java.security.spec.ECGenParameterSpec;
import java.util.Base64;

public class ECCEncription
{

    // Global variables
    private static final String RSA_ALGORITHM = "RSA";
    private static KeyPair keyPair;
    private static Cipher iesCipher;
    private static Cipher iesDecipher;


    //Constrator function start
    public ECCEncription()
    {
        try
        {
            GenerateKey();

            iesCipher = Cipher.getInstance("ECIESwithAES-CBC");
            iesDecipher = Cipher.getInstance("ECIESwithAES-CBC");
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
        Security.addProvider(new BouncyCastleProvider());

        KeyPairGenerator ecKeyGen = KeyPairGenerator.getInstance("EC",BouncyCastleProvider.PROVIDER_NAME);
        ecKeyGen.initialize(new ECGenParameterSpec("secp256r1"));

        keyPair = ecKeyGen.generateKeyPair();

        return Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded());
    }
    //Get generate key function end

    //Get encrption function start
    public ECC_Encription_Model Encription(String Value) throws Exception
    {
        SecureRandom random = new SecureRandom();
        byte [] nonce = new byte[16];
        random.nextBytes(nonce);
        IESParameterSpec iesParamSpec = new IESParameterSpec(null, null, 256, 256, nonce, false);

        // enrypt message
        iesCipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic(),  iesParamSpec);
        byte[] ciphertext = iesCipher.doFinal(Value.getBytes());
        //System.out.println(Base64.getEncoder().encodeToString(ciphertext));

        return new ECC_Encription_Model(new String(ciphertext),Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded()));
    }
    //Get encrption function end

    //Get decrption function start
    public String Decription(String Value) throws Exception
    {
        SecureRandom random = new SecureRandom();
        byte [] nonce = new byte[16];
        random.nextBytes(nonce);

        // enrypt message
        IESParameterSpec iesParamSpec = new IESParameterSpec(null, null, 256, 256, nonce, false);
        iesCipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic(),  iesParamSpec);
        //byte[] ciphertext = iesCipher.doFinal(Value.getBytes());
        //System.out.println(Base64.getEncoder().encodeToString(ciphertext));

        iesDecipher.init(Cipher.DECRYPT_MODE, keyPair.getPrivate(),iesCipher.getParameters());
        byte[] plaintext = iesDecipher.doFinal(Value.getBytes());

        System.out.println("DDDD "+new String(plaintext));

        return new String(plaintext);
    }
    //Get decrption function end

}
