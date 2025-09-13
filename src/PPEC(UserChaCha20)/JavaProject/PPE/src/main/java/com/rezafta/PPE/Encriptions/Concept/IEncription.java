package com.rezafta.PPE.Encriptions.Concept;

public interface IEncription
{
    public String GenerateKey() throws Exception;

    public String Encription(String Value,String TimeZone,String Salt) throws Exception;

    public String Decription(String Value,String TimeZone,String Salt) throws Exception;

}
