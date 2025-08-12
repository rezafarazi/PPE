package com.rezafta.PPE.Encriptions.Key;

import com.rezafta.PPE.Functions.TimeStep.TimeStep;

import java.util.Base64;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;


public class KeyGenerator
{


    //Get read time from url
    public static long getUnixTime() throws Exception
    {
        try
        {
            //String urlString = "https://worldtimeapi.org/api/timezone/Asia/Tehran";
            String urlString = "http://ip-api.com/json/?fields=status,message,timezone,offset";
            URL url = new URL(urlString);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Content-Type", "application/json");

            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String inputLine;
            StringBuilder content = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }

            in.close();
            conn.disconnect();

            JSONObject json = new JSONObject(content.toString());
            return json.getLong("offset");
        }
        catch (Exception e)
        {
            return 0;
        }
    }





    public static String GetCurrentTimeKey(String Salt)
    {
        String keybase="";
        String Dividedkeybase="";
        String Key="";

        long unix_time = 0;
        String timestep8="";

        try
        {
            unix_time = getUnixTime();
        }
        catch (Exception e)
        {

        }

        if(unix_time != 0)
        {
            timestep8 = (unix_time+"").substring(0,8);
        }
        else
        {
            long timestep = TimeStep.GetTimeStep();
            timestep8 = (timestep+"").substring(0,8);
        }


        char []timestep8char = timestep8.toCharArray();

        //System.out.println("time step is "+timestep);

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
            Key+=KeyChar;
        }

        Key = Salt + Key;
        Key=Key.substring(0,16);

        byte[] keyBytes = Key.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        String result = Base64.getEncoder().encodeToString(keyBytes);
        result = Base64.getEncoder().encodeToString(result.getBytes());
        //System.out.println(result);
        return result;
    }

}
