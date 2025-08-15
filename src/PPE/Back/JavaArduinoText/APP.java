import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class APP {

    public static void main(String[] args) {
        try {
            String key = "0123456789@ABCDE"; // کلید نمونه (باید با کلید آردوینو مطابقت داشته باشد)
            String encryptedBase64 = "1Ca4WUGCbG/BkLQqO5kvNZ4blMBCYlEc8SGplSXG4Kg="; // متن رمزگذاری شده Base64 را از آردوینو اینجا کپی کنید

            // Decode Base64
            byte[] cipherText = Base64.getDecoder().decode(encryptedBase64);

            // رمزگشایی AES
            SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(), "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(Cipher.DECRYPT_MODE, secretKey);

            byte[] decryptedBytes = cipher.doFinal(cipherText);
            String decryptedString = new String(decryptedBytes);

            System.out.println("Decrypted: " + decryptedString.trim()); // استفاده از trim برای حذف padding اضافی
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
