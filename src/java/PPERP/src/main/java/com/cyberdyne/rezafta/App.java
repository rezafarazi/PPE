package com.cyberdyne.rezafta;

import com.cyberdyne.rezafta.PPERP.Encriptions.Key.KeyGenerator;
import com.cyberdyne.rezafta.PPERP.Functions.TimeStep.TimeStep;
import com.cyberdyne.rezafta.PPERP.Models.AES_Encription_Model;
import com.cyberdyne.rezafta.PPERP.PPERP;
import com.cyberdyne.rezafta.PPERP.Types.EncriptionTypes;

import java.sql.Date;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class App
{

    //Main function start
    public static void main( String[] args ) throws Exception
    {

        String H="Hello world";
        PPERP p=new PPERP();
        AES_Encription_Model m = (AES_Encription_Model) p.GetEncription(H, EncriptionTypes.AES);

        String dec = p.GetDecription(m.getValue(),"",EncriptionTypes.AES);


        System.out.println("En is "+m.getValue());
        System.out.println("De is "+dec);

    }
    //Main function end

}
