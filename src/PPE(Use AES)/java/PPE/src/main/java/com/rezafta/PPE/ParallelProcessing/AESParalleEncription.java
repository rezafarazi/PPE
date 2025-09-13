package com.rezafta.PPE.ParallelProcessing;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import java.util.concurrent.RecursiveTask;


public class AESParalleEncription extends RecursiveTask<String>
{

    private static AESEncription AES=new AESEncription();

    String VALUE;
    String Salt;

    String TimeZone;

    public String getVALUE() {
        return VALUE;
    }

    public void setVALUE(String VALUE) {
        this.VALUE = VALUE;
    }

    public String getSalt() {
        return Salt;
    }

    public void setSalt(String salt) {
        Salt = salt;
    }

    public String getTimeZone() {
        return TimeZone;
    }

    public void setTimeZone(String timeZone) {
        TimeZone = timeZone;
    }

    public AESParalleEncription()
    {
    }

    public AESParalleEncription(String VALUE,String TimeZone, String salt)
    {
        this.VALUE = VALUE;
        this.Salt = salt;
        this.TimeZone = TimeZone;
    }

    @Override
    protected String compute()
    {
        try
        {
            return AES.Encription(VALUE,TimeZone,Salt);
        }
        catch (Exception e)
        {

        }
        return "";
    }
}
