package com.cyberdyne.rezafta.PPERP.PPERP.Models;

public class AES_Encription_Model
{

    String Key;
    String Value;

    public AES_Encription_Model(String value, String key)
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
