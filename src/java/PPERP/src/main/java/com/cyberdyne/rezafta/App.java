package com.cyberdyne.rezafta;

import com.cyberdyne.rezafta.PPERP.Models.Encription_Model;
import com.cyberdyne.rezafta.PPERP.PPERP;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

public class App
{


    //Main function start
    public static void main( String[] args ) throws Exception
    {

        String plainText = "Hello, AES!";

        Encription_Model Encrp = new PPERP().GetEncription(plainText, EncriptionTypes.AES);
        System.out.println("Result "+ Encrp.getValue());

        String Decip = new PPERP().GetDecription(Encrp.getValue(),Encrp.getKey(), EncriptionTypes.AES);
        System.out.println("Result "+ Decip);
    }
    //Main function end


}
