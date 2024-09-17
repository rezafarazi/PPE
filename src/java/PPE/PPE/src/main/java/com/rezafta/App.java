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
        String result=p.GetEncription("Hello world", "Asia/Tehran",EncriptionTypes.AES);

        String results=p.GetDecription(result,"Asia/Tehran",EncriptionTypes.AES);

        System.out.println("En last is : "+result);
        System.out.println("De last is : "+results);


    }

}
