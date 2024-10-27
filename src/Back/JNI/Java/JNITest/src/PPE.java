public class PPE
{

    public native String GetEncrypt(String VALUE);

    static {
        System.loadLibrary("PPE");
    }

}
