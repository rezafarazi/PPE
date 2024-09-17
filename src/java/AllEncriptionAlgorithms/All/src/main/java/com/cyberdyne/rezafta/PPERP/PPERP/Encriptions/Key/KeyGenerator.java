package com.cyberdyne.rezafta.PPERP.PPERP.Encriptions.Key;

import com.cyberdyne.rezafta.PPERP.PPERP.Functions.TimeStep.TimeStep;

import java.util.Base64;

public class KeyGenerator
{

    public static String GetCurrentTimeKey(String TimeZone)
    {
        String keybase="";
        String Dividedkeybase="";
        String Key="";

        long timestep = TimeStep.GetTimeStep(TimeZone);
        String timestep8 = (timestep+"").substring(0,8);
        char []timestep8char = timestep8.toCharArray();

        //Get keybase fist 8 number
        keybase = timestep8 ;

        for(int i = timestep8char.length-1; i >= 0 ; i--)
        {
            keybase += timestep8char[i];
        }

        for(int i = 0; i <= timestep8char.length-1 ; i++)
        {
            keybase += timestep8char[i];
        }

        for(int i = timestep8char.length-1; i >= 0 ; i--)
        {
            keybase += timestep8char[i];
        }

        for(int i = 0; i <= timestep8char.length-1 ; i++)
        {
            keybase += timestep8char[i];
        }

        for(int i = timestep8char.length-1; i >= 0 ; i--)
        {
            keybase += timestep8char[i];
        }

        for(int i = 0; i <= timestep8char.length-1 ; i++)
        {
            keybase += timestep8char[i];
        }

        for(int i = timestep8char.length-1; i >= 0 ; i--)
        {
            keybase += timestep8char[i];
        }

        for(int i = 0; i <= timestep8char.length-1 ; i++)
        {
            keybase += timestep8char[i];
        }

        char []keybasechar=keybase.toCharArray();
        for(int i = 0; i <= keybasechar.length / 2 ; i+=2)
        {
            String NumA,NumB;
            NumA = keybasechar[i]+"";
            NumB = keybasechar[i+1]+"";

            int AddNum=Integer.parseInt(NumA+NumB);
            char KeyChar=(char) AddNum;
//            System.out.println(KeyChar);
            Key+=KeyChar;
        }

        Key=Key.substring(0,16);
        System.out.println(Key.length());

        return Base64.getEncoder().encodeToString(Key.getBytes());
    }

}
