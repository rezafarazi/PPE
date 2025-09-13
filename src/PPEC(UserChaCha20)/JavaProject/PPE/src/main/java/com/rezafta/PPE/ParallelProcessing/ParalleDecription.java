package com.rezafta.PPE.ParallelProcessing;

import com.rezafta.PPE.Encriptions.Algorithm.AESEncription;
import com.rezafta.PPE.Encriptions.Algorithm.ChaCha20Encryption;
import com.rezafta.PPE.Encriptions.Concept.IEncription;
import com.rezafta.PPE.Types.EncriptionTypes;

import java.util.concurrent.RecursiveTask;


public class ParalleDecription extends RecursiveTask<String>
{

    IEncription EncriptionService;

    EncriptionTypes Type;
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

    public EncriptionTypes getType() {
        return Type;
    }

    public void setType(EncriptionTypes type) {
        Type = type;
    }

    public ParalleDecription()
    {
    }

    public ParalleDecription(EncriptionTypes Type, String VALUE, String Timezone, String salt)
    {
        this.VALUE = VALUE;
        this.Salt = salt;
        this.TimeZone=Timezone;
        this.Type=Type;

        switch (Type)
        {
            case AES:
                EncriptionService = new AESEncription();
                break;
            case ChaCha20:
                EncriptionService = new ChaCha20Encryption();
                break;
        }
    }

    @Override
    protected String compute()
    {
        try
        {
            return EncriptionService.Decription(VALUE,TimeZone,Salt);
        }
        catch (Exception e)
        {

        }
        return "";
    }
}
