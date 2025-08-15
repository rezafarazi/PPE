package com.rezafta;

import com.rezafta.PPE.PPE;
import com.rezafta.PPE.Types.EncriptionTypes;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args ) throws Exception
    {

        PPE p=new PPE();
        String result=p.GetEncription("salam", "reza",EncriptionTypes.AES);
        System.out.println("En last is : "+result);

        String results=p.GetDecription(result,"reza",EncriptionTypes.AES);
        System.out.println("De last is : "+results);

    }

}
