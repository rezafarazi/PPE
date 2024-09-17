package com.rezafta.PPE.Functions.TimeStep;

import org.json.JSONObject;

import java.io.*;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class TimeStep
{

    public static long GetTimeStep()
    {

//            Time zone not exactly sync
//            ZonedDateTime TimeZone=ZonedDateTime.now(ZoneId.of(timezone));
//            LocalDateTime TimeZoneLocalDateTime = TimeZone.toLocalDateTime();
//            Timestamp TimeStep=Timestamp.valueOf(TimeZoneLocalDateTime);

//
//        try
//        {
//            String websiteURL = "https://worldtimeapi.org/api/timezone/"+timezone; // Replace with your desired URL
//
//            URL url = new URL(websiteURL);
//            URLConnection urlConnection = url.openConnection();
//
//            // Set up SSL connection
//            urlConnection.setConnectTimeout(5000); // Timeout after 5 seconds
//            urlConnection.setReadTimeout(5000); // Read timeout after 5 seconds
//
//            // Get the input stream
//            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
//            String inputLine;
//            String buffer="";
//            while ((inputLine = in.readLine()) != null)
//            {
//                buffer+=inputLine;
////                System.out.println(inputLine);
//            }
//            in.close();
//
//            JSONObject Times=new JSONObject(buffer);
//
//            return Long.parseLong(Times.getInt("unixtime")+"");
//        }
//        catch (Exception e)
//        {
//            System.out.println("Error : "+e.getMessage());
//            return 0;
//        }

        long unixTime = System.currentTimeMillis() / 1000L;
        return unixTime;
    }


}
