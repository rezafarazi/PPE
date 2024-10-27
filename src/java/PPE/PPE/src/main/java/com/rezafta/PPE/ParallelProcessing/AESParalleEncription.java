package com.rezafta.PPE.ParallelProcessing;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import java.util.concurrent.RecursiveTask;


public class AESParalleEncription extends RecursiveTask<String>
{

    private static AESEncription AES=new AESEncription();

    String VALUE;
    String Salt;

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

    public AESParalleEncription()
    {
    }

    public AESParalleEncription(String VALUE, String salt)
    {
        this.VALUE = VALUE;
        Salt = salt;
    }

    @Override
    protected String compute()
    {
        try
        {
            return AES.Encription(VALUE,Salt);
        }
        catch (Exception e)
        {

        }
        return "";
    }
}
