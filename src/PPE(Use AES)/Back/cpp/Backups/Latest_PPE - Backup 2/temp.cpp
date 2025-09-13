std::string GETPPE(std::string VALUE,std::string KEY,int Mode)
{
    // the expanded keySize
    int expandedKeySize = 176;

    // the expanded key
    unsigned char expandedKey[expandedKeySize];

    // the cipher key
    unsigned char key[24]; // Assuming key has enough space for the string
    for (size_t i = 0; i < 24; ++i) {
        key[i] = static_cast<unsigned char>(KEY[i]);
    }
    key[KEY.size()] = '\0';

    // the cipher key size
    enum keySize size = SIZE_24;


    if(Mode == 1)
    {

        size_t length = VALUE.length();
        size_t halfLength = length / 2;

        // Create an unsigned char array with double the length of the input string
        unsigned char* CharArray_A = new unsigned char[halfLength];
        unsigned char* CharArray_B = new unsigned char[halfLength];

        // Copy the first half of the string to the first half of the char array
        for (size_t i = 0; i < halfLength; ++i) {
            CharArray_A[i] = static_cast<unsigned char>(VALUE[i]);
        }

        // Copy the second half of the string to the second half of the char array
        int j=0;
        for (size_t i = halfLength; i < length; ++i)
        {
            CharArray_B[j] = static_cast<unsigned char>(VALUE[i]);
            j++;
        }

        std::cout<<"a is : "<<CharArray_A<<"\n";
        std::cout<<"b is : "<<CharArray_B<<"\n";

        // the ciphertext
        unsigned char ciphertext_A[halfLength];
        unsigned char ciphertext_B[halfLength];

        // Test the Key Expansion
        expandKey(expandedKey, key, size, expandedKeySize);

        // AES Encryption
        aes_encrypt(CharArray_A, ciphertext_A, key, SIZE_24);
        aes_encrypt(CharArray_B, ciphertext_B, key, SIZE_24);

        std::string result_A(reinterpret_cast<char*>(ciphertext_A), sizeof halfLength );
        std::string result_B(reinterpret_cast<char*>(ciphertext_B), sizeof halfLength );

        //std::string result=result_A+"~|~"+result_B;

        //return base64_encode(result);
        return result_A;
    }

    if(Mode == 0)
    {
/*
        size_t length = VALUE.length();
        size_t halfLength = length / 2;

        //the clipher
        const char* encoded_string = VALUE.c_str(); // Example Base64-encoded string
        size_t encoded_length = strlen(encoded_string);
        size_t decoded_length;



        unsigned char* ciphertext = new unsigned char[length];
        for (int i = 0; i < length; ++i) {
            ciphertext[i]=VALUE[i];
        }
        std::cout<<"RRRRRR : "<<VALUE;
        /*const char* delimiter = "~|~";
        unsigned char* ciphertext = base64_decode(encoded_string, encoded_length, &decoded_length);
        char* cipher = (char*)ciphertext;
        unsigned char* ciphertext_A = (unsigned char*) strtok(cipher,delimiter);
        unsigned char* ciphertext_B = (unsigned char*) strtok(NULL,delimiter);*/



        // the ciphertext
        //unsigned char decryptedtext[sizeof VALUE];
        /*      unsigned char decryptedtext_A[halfLength];
              unsigned char decryptedtext_B[halfLength];

              // Test the Key Expansion
              expandKey(expandedKey, key, size, expandedKeySize);

              // AES Decryption
              //aes_decrypt(ciphertext, decryptedtext, key, SIZE_24);
              aes_decrypt(ciphertext, decryptedtext_A, key, SIZE_24);
              //aes_decrypt(ciphertext_B, decryptedtext_B, key, SIZE_24);

              std::cout<<"\n Left is  : "<<decryptedtext_A<<"\n";
              std::cout<<"\n Right is : "<<decryptedtext_B<<"\n";

              std::string result="";
              for (int i = 0; i < sizeof decryptedtext_A ;i++)
              {
                  result+=decryptedtext_A[i];
              }
              for (int i = 0; i < sizeof decryptedtext_B ;i++)
              {
                  result+=decryptedtext_B[i];
              }

              return result;*/
    }

    return "";
}