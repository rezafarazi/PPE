package com.cyberdyne.rezafta.PPERP.Models;

public class RSA_Encription_Model
{

    String Key;
    String Value;

    public RSA_Encription_Model(String value, String key)
    {
        Key = key;
        Value = value;
    }

    public String getKey() {
        return Key;
    }

    public void setKey(String key) {
        Key = key;
    }

    public String getValue() {
        return Value;
    }

    public void setValue(String value) {
        Value = value;
    }
}
