#include <iostream>
#include <string>
#include <ctime>
#include <vector>
#include <sstream>
#include <iomanip>
#include <string.h>
#include <windows.h>

/********************Generate Key start**********************/
static const std::string base64_chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/";

static const unsigned char b64_table[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// Function to decode Base64 and return as std::string
std::string base64_decode_to_string(const std::string& input) {
    const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    size_t input_len = input.length();
    std::vector<uint8_t> output;

    for (size_t i = 0; i < input_len; i += 4) {
        uint32_t block = 0;
        for (int j = 0; j < 4; ++j) {
            char c = input[i + j];
            if (c == '=')
                break;
            auto pos = base64_chars.find(c);
            if (pos != std::string::npos)
                block = (block << 6) | static_cast<uint32_t>(pos);
        }

        output.push_back((block >> 16) & 0xFF);
        if (input[i + 2] != '=')
            output.push_back((block >> 8) & 0xFF);
        if (input[i + 3] != '=')
            output.push_back(block & 0xFF);
    }

    return std::string(output.begin(), output.end());
}

unsigned char* base64_decode(const char* data, size_t input_length, size_t* output_length) {
    if (input_length % 4 != 0) return NULL;

    *output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=') (*output_length)--;
    if (data[input_length - 2] == '=') (*output_length)--;

    unsigned char* decoded_data = (unsigned char*)malloc(*output_length + 1); // Explicit cast to unsigned char*
    if (decoded_data == NULL) return NULL;

    for (size_t i = 0, j = 0; i < input_length;) {
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : strchr((const char*)b64_table, data[i++]) - (const char*)b64_table;
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : strchr((const char*)b64_table, data[i++]) - (const char*)b64_table;
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : strchr((const char*)b64_table, data[i++]) - (const char*)b64_table;
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : strchr((const char*)b64_table, data[i++]) - (const char*)b64_table;

        uint32_t triple = (sextet_a << 3 * 6) + (sextet_b << 2 * 6) + (sextet_c << 1 * 6) + (sextet_d << 0 * 6);

        if (j < *output_length) decoded_data[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 0 * 8) & 0xFF;
    }

    decoded_data[*output_length] = '\0'; // Null-terminate the string
    return decoded_data;
}

std::string base64_encode(const std::string& in)
{
    std::string out;
    int val = 0, valb = -6;
    for (unsigned char c : in) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) out.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    while (out.size() % 4) out.push_back('=');
    return out;
}

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

long GetTimeStep() {

    time_t current_time;
    struct tm gmt_time;
    current_time = time(NULL);
    if (gmtime_s(&gmt_time, &current_time) != 0)
    {
        perror("gmtime_s");
        return 1;
    }
    //printf("Current GMT Unix time: %ld\n", (long)current_time);

    return (long)current_time;
}

std::string GetCurrentTimeKey(const std::string& Slat, bool based)
{
    std::string keybase;
    std::string Key;

    long timestep = GetTimeStep();
    std::string timestep8 = std::to_string(timestep).substr(0, 8);
    std::vector<char> timestep8char(timestep8.begin(), timestep8.end());

    keybase = timestep8;

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    for (int i = timestep8char.size() - 1; i >= 0; --i) {
        keybase += timestep8char[i];
    }

    for (int i = 0; i < timestep8char.size(); ++i) {
        keybase += timestep8char[i];
    }

    std::vector<char> keybasechar(keybase.begin(), keybase.end());
    for (size_t i = 0; i <= keybasechar.size() / 2; i += 2) {
        std::string NumA(1, keybasechar[i]);
        std::string NumB(1, keybasechar[i + 1]);

        int AddNum = std::stoi(NumA + NumB);
        char KeyChar = static_cast<char>(AddNum);
        Key += KeyChar;
    }

    Key += Slat;

    Key = Key.substr(0, 24);

    if (based)
    {
        std::string encodedKey = base64_encode(Key);
        //std::cout << encodedKey;
        return encodedKey;
    }
    else
    {
        return Key;
    }
}
/********************Generate Key end**********************/


/********************AES start**********************/
/* Basic implementation of AES in C
*
* Warning: THIS CODE IS ONLY FOR LEARNING PURPOSES
*          NOT RECOMMENDED TO USE IT IN ANY PRODUCTS
*/

#include <stdio.h>  // for printf
#include <stdlib.h> // for malloc, free

enum errorCode
{
    SUCCESS = 0,
    ERROR_AES_UNKNOWN_KEYSIZE,
    ERROR_MEMORY_ALLOCATION_FAILED,
};

// Implementation: S-Box

unsigned char sbox[256] = {
        // 0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  // 0
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  // 1
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  // 2
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  // 3
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  // 4
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  // 5
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  // 6
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  // 7
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  // 8
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  // 9
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  // A
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  // B
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  // C
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  // D
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  // E
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16}; // F

unsigned char rsbox[256] =
        {0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d};

unsigned char getSBoxValue(unsigned char num);
unsigned char getSBoxInvert(unsigned char num);

// Implementation: Rotate
void rotate(unsigned char *word);

// Implementation: Rcon
unsigned char Rcon[255] = {
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
        0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
        0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
        0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
        0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
        0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
        0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
        0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02,
        0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
        0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
        0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33,
        0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb};

unsigned char getRconValue(unsigned char num);

// Implementation: Key Schedule Core
void core(unsigned char *word, int iteration);

// Implementation: Key Expansion

enum keySize
{
    SIZE_16 = 16,
    SIZE_24 = 24,
    SIZE_32 = 32
};

void expandKey(unsigned char *expandedKey, unsigned char *key, enum keySize, size_t expandedKeySize);

// Implementation: AES Encryption

// Implementation: subBytes
void subBytes(unsigned char *state);
// Implementation: shiftRows
void shiftRows(unsigned char *state);
void shiftRow(unsigned char *state, unsigned char nbr);
// Implementation: addRoundKey
void addRoundKey(unsigned char *state, unsigned char *roundKey);
// Implementation: mixColumns
unsigned char galois_multiplication(unsigned char a, unsigned char b);
void mixColumns(unsigned char *state);
void mixColumn(unsigned char *column);
// Implementation: AES round
void aes_round(unsigned char *state, unsigned char *roundKey);
// Implementation: the main AES body
void createRoundKey(unsigned char *expandedKey, unsigned char *roundKey);
void aes_main(unsigned char *state, unsigned char *expandedKey, int nbrRounds);
// Implementation: AES encryption
char aes_encrypt(unsigned char *input, unsigned char *output, unsigned char *key, enum keySize size);
// AES Decryption
void invSubBytes(unsigned char *state);
void invShiftRows(unsigned char *state);
void invShiftRow(unsigned char *state, unsigned char nbr);
void invMixColumns(unsigned char *state);
void invMixColumn(unsigned char *column);
void aes_invRound(unsigned char *state, unsigned char *roundKey);
void aes_invMain(unsigned char *state, unsigned char *expandedKey, int nbrRounds);
char aes_decrypt(unsigned char *input, unsigned char *output, unsigned char *key, enum keySize size);

std::string GETPPESINGLE(std::string VALUE,std::string KEY,int Mode)
{
    // the expanded keySize
    int expandedKeySize = 192;

    // the expanded key
    unsigned char expandedKey[expandedKeySize];

    // the cipher key
    unsigned char key[24]; // Assuming key has enough space for the string
    for (size_t i = 0; i < 24; i++) {
        key[i] = static_cast<unsigned char>(KEY[i]);
    }
    key[KEY.size()] = '\0';

    // the cipher key size
    enum keySize size = SIZE_24;


    if(Mode == 1)
    {
        // the plaintext
        const int VAL_LEN = VALUE.length();
        unsigned char plaintext[sizeof VALUE];
        for(int i=0;i<=sizeof plaintext;i++)
        {
            if(VAL_LEN > i)
            {
                plaintext[i] = VALUE[i];
            }
            else
            {
                plaintext[i] = ' ';
            }
        }

        // the ciphertext
        unsigned char ciphertext[sizeof VALUE];

        // Test the Key Expansion
        expandKey(expandedKey, key, size, expandedKeySize);

        // AES Encryption
        aes_encrypt(plaintext, ciphertext, key, SIZE_24);


        std::string result="";
        for (int i = 0; i < sizeof ciphertext; i++)
        {
            if(ciphertext[i] == NULL)
            {
                result+=0xcb;
            }
            else
            {
                result+=ciphertext[i];
                //std::cout << ciphertext[i] << "-";
            }
        }

        //        std::string result(reinterpret_cast<char*>(ciphertext), sizeof VALUE);
        return base64_encode(result);
    }

    if(Mode == 0)
    {
        VALUE = base64_decode_to_string(VALUE);
        //the clipher
        char VAL[1024];
        strcpy(VAL,VALUE.c_str());
        unsigned char* ciphertext = reinterpret_cast<unsigned char*>(VAL);


        // the ciphertext
        unsigned char decryptedtext[sizeof VALUE];

        // Test the Key Expansion
        expandKey(expandedKey, key, size, expandedKeySize);

        // AES Decryption
        aes_decrypt(ciphertext, decryptedtext, key, SIZE_24);

        std::string result="";
        for (int i = 0; i < sizeof decryptedtext ;i++)
        {
            result+=decryptedtext[i];
        }
        return result;
    }

    return "";
}

unsigned char getSBoxValue(unsigned char num)
{
    return sbox[num];
}

unsigned char getSBoxInvert(unsigned char num)
{
    return rsbox[num];
}

/* Rijndael's key schedule rotate operation
* rotate the word eight bits to the left
*
* rotate(1d2c3a4f) = 2c3a4f1d
*
* word is an char array of size 4 (32 bit)
*/
void rotate(unsigned char *word)
{
    unsigned char c;
    int i;

    c = word[0];
    for (i = 0; i < 3; i++)
        word[i] = word[i + 1];
    word[3] = c;
}

unsigned char getRconValue(unsigned char num)
{
    return Rcon[num];
}

void core(unsigned char *word, int iteration)
{
    int i;

    // rotate the 32-bit word 8 bits to the left
    rotate(word);

    // apply S-Box substitution on all 4 parts of the 32-bit word
    for (i = 0; i < 4; ++i)
    {
        word[i] = getSBoxValue(word[i]);
    }

    // XOR the output of the rcon operation with i to the first part (leftmost) only
    word[0] = word[0] ^ getRconValue(iteration);
}

/* Rijndael's key expansion
* expands an 128,192,256 key into an 176,208,240 bytes key
*
* expandedKey is a pointer to an char array of large enough size
* key is a pointer to a non-expanded key
*/

void expandKey(unsigned char *expandedKey,
               unsigned char *key,
               enum keySize size,
               size_t expandedKeySize)
{
    // current expanded keySize, in bytes
    int currentSize = 0;
    int rconIteration = 1;
    int i;
    unsigned char t[4] = {0}; // temporary 4-byte variable

    // set the 16,24,32 bytes of the expanded key to the input key
    for (i = 0; i < size; i++)
        expandedKey[i] = key[i];
    currentSize += size;

    while (currentSize < expandedKeySize)
    {
        // assign the previous 4 bytes to the temporary value t
        for (i = 0; i < 4; i++)
        {
            t[i] = expandedKey[(currentSize - 4) + i];
        }

        /* every 16,24,32 bytes we apply the core schedule to t
        * and increment rconIteration afterwards
        */
        if (currentSize % size == 0)
        {
            core(t, rconIteration++);
        }

        // For 256-bit keys, we add an extra sbox to the calculation
        if (size == SIZE_32 && ((currentSize % size) == 16))
        {
            for (i = 0; i < 4; i++)
                t[i] = getSBoxValue(t[i]);
        }

        /* We XOR t with the four-byte block 16,24,32 bytes before the new expanded key.
        * This becomes the next four bytes in the expanded key.
        */
        for (i = 0; i < 4; i++)
        {
            expandedKey[currentSize] = expandedKey[currentSize - size] ^ t[i];
            currentSize++;
        }
    }
}

void subBytes(unsigned char *state)
{
    int i;
    /* substitute all the values from the state with the value in the SBox
    * using the state value as index for the SBox
    */
    for (i = 0; i < 16; i++)
        state[i] = getSBoxValue(state[i]);
}

void shiftRows(unsigned char *state)
{
    int i;
    // iterate over the 4 rows and call shiftRow() with that row
    for (i = 0; i < 4; i++)
        shiftRow(state + i * 4, i);
}

void shiftRow(unsigned char *state, unsigned char nbr)
{
    int i, j;
    unsigned char tmp;
    // each iteration shifts the row to the left by 1
    for (i = 0; i < nbr; i++)
    {
        tmp = state[0];
        for (j = 0; j < 3; j++)
            state[j] = state[j + 1];
        state[3] = tmp;
    }
}

void addRoundKey(unsigned char *state, unsigned char *roundKey)
{
    int i;
    for (i = 0; i < 16; i++)
        state[i] = state[i] ^ roundKey[i];
}

unsigned char galois_multiplication(unsigned char a, unsigned char b)
{
    unsigned char p = 0;
    unsigned char counter;
    unsigned char hi_bit_set;
    for (counter = 0; counter < 8; counter++)
    {
        if ((b & 1) == 1)
            p ^= a;
        hi_bit_set = (a & 0x80);
        a <<= 1;
        if (hi_bit_set == 0x80)
            a ^= 0x1b;
        b >>= 1;
    }
    return p;
}

void mixColumns(unsigned char *state)
{
    int i, j;
    unsigned char column[4];

    // iterate over the 4 columns
    for (i = 0; i < 4; i++)
    {
        // construct one column by iterating over the 4 rows
        for (j = 0; j < 4; j++)
        {
            column[j] = state[(j * 4) + i];
        }

        // apply the mixColumn on one column
        mixColumn(column);

        // put the values back into the state
        for (j = 0; j < 4; j++)
        {
            state[(j * 4) + i] = column[j];
        }
    }
}

void mixColumn(unsigned char *column)
{
    unsigned char cpy[4];
    int i;
    for (i = 0; i < 4; i++)
    {
        cpy[i] = column[i];
    }
    column[0] = galois_multiplication(cpy[0], 2) ^
                galois_multiplication(cpy[3], 1) ^
                galois_multiplication(cpy[2], 1) ^
                galois_multiplication(cpy[1], 3);

    column[1] = galois_multiplication(cpy[1], 2) ^
                galois_multiplication(cpy[0], 1) ^
                galois_multiplication(cpy[3], 1) ^
                galois_multiplication(cpy[2], 3);

    column[2] = galois_multiplication(cpy[2], 2) ^
                galois_multiplication(cpy[1], 1) ^
                galois_multiplication(cpy[0], 1) ^
                galois_multiplication(cpy[3], 3);

    column[3] = galois_multiplication(cpy[3], 2) ^
                galois_multiplication(cpy[2], 1) ^
                galois_multiplication(cpy[1], 1) ^
                galois_multiplication(cpy[0], 3);
}

void aes_round(unsigned char *state, unsigned char *roundKey)
{
    subBytes(state);
    shiftRows(state);
    mixColumns(state);
    addRoundKey(state, roundKey);
}

void createRoundKey(unsigned char *expandedKey, unsigned char *roundKey)
{
    int i, j;
    // iterate over the columns
    for (i = 0; i < 4; i++)
    {
        // iterate over the rows
        for (j = 0; j < 4; j++)
            roundKey[(i + (j * 4))] = expandedKey[(i * 4) + j];
    }
}

void aes_main(unsigned char *state, unsigned char *expandedKey, int nbrRounds)
{
    int i = 0;

    unsigned char roundKey[16];

    createRoundKey(expandedKey, roundKey);
    addRoundKey(state, roundKey);

    for (i = 1; i < nbrRounds; i++)
    {
        createRoundKey(expandedKey + 16 * i, roundKey);
        aes_round(state, roundKey);
    }

    createRoundKey(expandedKey + 16 * nbrRounds, roundKey);
    subBytes(state);
    shiftRows(state);
    addRoundKey(state, roundKey);
}

char aes_encrypt(unsigned char *input,
                 unsigned char *output,
                 unsigned char *key,
                 enum keySize size)
{
    // the expanded keySize
    int expandedKeySize;

    // the number of rounds
    int nbrRounds;

    // the expanded key
    unsigned char *expandedKey;

    // the 128 bit block to encode
    unsigned char block[16];

    int i, j;

    // set the number of rounds
    switch (size)
    {
        case SIZE_16:
            nbrRounds = 10;
            break;
        case SIZE_24:
            nbrRounds = 12;
            break;
        case SIZE_32:
            nbrRounds = 14;
            break;
        default:
            return ERROR_AES_UNKNOWN_KEYSIZE;
            break;
    }

    expandedKeySize = (16 * (nbrRounds + 1));

    expandedKey = (unsigned char *)malloc(expandedKeySize * sizeof(unsigned char));

    if (expandedKey == NULL)
    {
        return ERROR_MEMORY_ALLOCATION_FAILED;
    }
    else
    {
        /* Set the block values, for the block:
        * a0,0 a0,1 a0,2 a0,3
        * a1,0 a1,1 a1,2 a1,3
        * a2,0 a2,1 a2,2 a2,3
        * a3,0 a3,1 a3,2 a3,3
        * the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        */

        // iterate over the columns
        for (i = 0; i < 4; i++)
        {
            // iterate over the rows
            for (j = 0; j < 4; j++)
                block[(i + (j * 4))] = input[(i * 4) + j];
        }

        // expand the key into an 176, 208, 240 bytes key
        expandKey(expandedKey, key, size, expandedKeySize);

        // encrypt the block using the expandedKey
        aes_main(block, expandedKey, nbrRounds);

        // unmap the block again into the output
        for (i = 0; i < 4; i++)
        {
            // iterate over the rows
            for (j = 0; j < 4; j++)
                output[(i * 4) + j] = block[(i + (j * 4))];
        }

        // de-allocate memory for expandedKey
        free(expandedKey);
        expandedKey = NULL;
    }

    return SUCCESS;
}

void invSubBytes(unsigned char *state)
{
    int i;
    /* substitute all the values from the state with the value in the SBox
    * using the state value as index for the SBox
    */
    for (i = 0; i < 16; i++)
        state[i] = getSBoxInvert(state[i]);
}

void invShiftRows(unsigned char *state)
{
    int i;
    // iterate over the 4 rows and call invShiftRow() with that row
    for (i = 0; i < 4; i++)
        invShiftRow(state + i * 4, i);
}

void invShiftRow(unsigned char *state, unsigned char nbr)
{
    int i, j;
    unsigned char tmp;
    // each iteration shifts the row to the right by 1
    for (i = 0; i < nbr; i++)
    {
        tmp = state[3];
        for (j = 3; j > 0; j--)
            state[j] = state[j - 1];
        state[0] = tmp;
    }
}

void invMixColumns(unsigned char *state)
{
    int i, j;
    unsigned char column[4];

    // iterate over the 4 columns
    for (i = 0; i < 4; i++)
    {
        // construct one column by iterating over the 4 rows
        for (j = 0; j < 4; j++)
        {
            column[j] = state[(j * 4) + i];
        }

        // apply the invMixColumn on one column
        invMixColumn(column);

        // put the values back into the state
        for (j = 0; j < 4; j++)
        {
            state[(j * 4) + i] = column[j];
        }
    }
}

void invMixColumn(unsigned char *column)
{
    unsigned char cpy[4];
    int i;
    for (i = 0; i < 4; i++)
    {
        cpy[i] = column[i];
    }
    column[0] = galois_multiplication(cpy[0], 14) ^
                galois_multiplication(cpy[3], 9) ^
                galois_multiplication(cpy[2], 13) ^
                galois_multiplication(cpy[1], 11);
    column[1] = galois_multiplication(cpy[1], 14) ^
                galois_multiplication(cpy[0], 9) ^
                galois_multiplication(cpy[3], 13) ^
                galois_multiplication(cpy[2], 11);
    column[2] = galois_multiplication(cpy[2], 14) ^
                galois_multiplication(cpy[1], 9) ^
                galois_multiplication(cpy[0], 13) ^
                galois_multiplication(cpy[3], 11);
    column[3] = galois_multiplication(cpy[3], 14) ^
                galois_multiplication(cpy[2], 9) ^
                galois_multiplication(cpy[1], 13) ^
                galois_multiplication(cpy[0], 11);
}

void aes_invRound(unsigned char *state, unsigned char *roundKey)
{

    invShiftRows(state);
    invSubBytes(state);
    addRoundKey(state, roundKey);
    invMixColumns(state);
}

void aes_invMain(unsigned char *state, unsigned char *expandedKey, int nbrRounds)
{
    int i = 0;

    unsigned char roundKey[16];

    createRoundKey(expandedKey + 16 * nbrRounds, roundKey);
    addRoundKey(state, roundKey);

    for (i = nbrRounds - 1; i > 0; i--)
    {
        createRoundKey(expandedKey + 16 * i, roundKey);
        aes_invRound(state, roundKey);
    }

    createRoundKey(expandedKey, roundKey);
    invShiftRows(state);
    invSubBytes(state);
    addRoundKey(state, roundKey);
}

char aes_decrypt(unsigned char *input,
                 unsigned char *output,
                 unsigned char *key,
                 enum keySize size)
{
    // the expanded keySize
    int expandedKeySize;

    // the number of rounds
    int nbrRounds;

    // the expanded key
    unsigned char *expandedKey;

    // the 128 bit block to decode
    unsigned char block[16];

    int i, j;

    // set the number of rounds
    switch (size)
    {
        case SIZE_16:
            nbrRounds = 10;
            break;
        case SIZE_24:
            nbrRounds = 12;
            break;
        case SIZE_32:
            nbrRounds = 14;
            break;
        default:
            return ERROR_AES_UNKNOWN_KEYSIZE;
            break;
    }

    expandedKeySize = (16 * (nbrRounds + 1));

    expandedKey = (unsigned char *)malloc(expandedKeySize * sizeof(unsigned char));

    if (expandedKey == NULL)
    {
        return ERROR_MEMORY_ALLOCATION_FAILED;
    }
    else
    {
        /* Set the block values, for the block:
        * a0,0 a0,1 a0,2 a0,3
        * a1,0 a1,1 a1,2 a1,3
        * a2,0 a2,1 a2,2 a2,3
        * a3,0 a3,1 a3,2 a3,3
        * the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        */

        // iterate over the columns
        for (i = 0; i < 4; i++)
        {
            // iterate over the rows
            for (j = 0; j < 4; j++)
                block[(i + (j * 4))] = input[(i * 4) + j];
        }

        // expand the key into an 176, 208, 240 bytes key
        expandKey(expandedKey, key, size, expandedKeySize);

        // decrypt the block using the expandedKey
        aes_invMain(block, expandedKey, nbrRounds);

        // unmap the block again into the output
        for (i = 0; i < 4; i++)
        {
            // iterate over the rows
            for (j = 0; j < 4; j++)
                output[(i * 4) + j] = block[(i + (j * 4))];
        }

        // de-allocate memory for expandedKey
        free(expandedKey);
        expandedKey = NULL;
    }

    return SUCCESS;
}
/********************AES end**********************/


/********************Other functions start**********************/

std::string GetENC(std::string VALUE, int VAL_LEN, std::string TIMEKEY)
{
    // the expanded keySize
    int expandedKeySize = 176;

    // the expanded key
    char expandedKey[expandedKeySize];

    // the cipher key
    char* key;
    strcpy(key, TIMEKEY.c_str());


    // the cipher key size
    enum keySize size = SIZE_16;

    // the plaintext
    char* plaintext;
    plaintext = (char*)malloc(VAL_LEN * sizeof(char));
    strcpy(plaintext, VALUE.c_str());

    // the ciphertext
    char* ciphertext;
    ciphertext = (char*)malloc(VAL_LEN * sizeof(char));

    int i;

    //    printf("\nCipher Key (HEX format):\n");
    //    for (i = 0; i < 16; i++)
    //    {
    //        // Print characters in HEX format, 16 chars per line
    //        printf("%2.2x%c", key[i], ((i + 1) % 16) ? ' ' : '\n');
    //    }
    //    std::cout << "\n---------------------------------------------------\n";

    for (i = 0; i < VAL_LEN; i++)
    {
        // Print characters in HEX format, 16 chars per line
        printf("%c", key[i], ((i + 1) % VAL_LEN) ? ' ' : '\n');
    }

    free(plaintext);
    free(ciphertext);

    return "";

}

std::string TrimString(std::string str) {
    const std::string whitespace = " \t\n\r\f\v"; // All types of possible spaces
    // Remove leading whitespace
    size_t firstNonSpace = str.find_first_not_of(whitespace);
    str.erase(0, firstNonSpace);
    // Remove trailing whitespace
    size_t lastNonSpace = str.find_last_not_of(whitespace);
    str.erase(lastNonSpace + 1);
    return str;
}

std::string convertUnsignedCharToString(const unsigned char* dataToSend, int sendLength) {
    std::ostringstream convertStream;
    convertStream << std::hex << std::setfill('0');

    for (int i = 0; i < sendLength; ++i) {
        convertStream << std::setw(2) << static_cast<short>(dataToSend[i]);
    }

    return convertStream.str();
}

std::string RemoveTempsString(std::string str) {
    std::string result="";
    int space_count=0;
    for (int i = 0; i < str.length(); i++)
    {
        if(str[i] == ' ')
        {
            space_count++;
            if(space_count>=2)
            {
                break;
            }
        }
        else
        {
            //std::cout<<space_count<<std::endl;
            if(space_count!=0)
            {
                for (int j = 0; j < space_count; j++)
                {
                    result+=" ";
                }
                space_count=0;
            }

            result+=str[i];
        }
    }
    return result;
}

void copyToClipboard(std::string val)
{
    const char *text=val.c_str();


    // Open the clipboard
    if (!OpenClipboard(NULL)) {
        printf("Failed to open clipboard\n");
        return;
    }

    // Empty the clipboard
    EmptyClipboard();

    // Allocate global memory for the text
    HGLOBAL hGlob = GlobalAlloc(GMEM_FIXED, strlen(text) + 1);
    if (!hGlob) {
        printf("Failed to allocate memory\n");
        CloseClipboard();
        return;
    }

    // Copy the text to the global memory
    strcpy((char*)hGlob, text);

    // Set the clipboard data
    SetClipboardData(CF_TEXT, hGlob);

    // Close the clipboard
    CloseClipboard();
    std::cout<<"Coped";
}

/********************Other functions end**********************/


/********************PPE functions start**********************/


//Get parallel processing function start
std::string GETPPE(std::string VALUE,std::string KEY,int Mode)
{
    if(Mode == 1)
    {
        //Get len of string
        int middleIndex = VALUE.length() / 2;

        //divided string 2
        std::string LeftSide = VALUE.substr(0, middleIndex);
        std::string RightSide = VALUE.substr(middleIndex);

        //Get encript
        std::string LeftEn=GETPPESINGLE(LeftSide,KEY,Mode);
        std::string RightEn=GETPPESINGLE(RightSide,KEY,Mode);

        return LeftEn+"~|~"+RightEn;
    }
    else if(Mode == 0)
    {

        std::istringstream iss(VALUE);
        std::string token;
        std::vector<std::string> tokens;

        while (std::getline(iss, token, '~')) {
            // Remove the trailing "|"
            if (!token.empty() && token.back() == '|') {
                token.pop_back();
            }
            tokens.push_back(token);
        }

        // Now 'tokens' contains the split substrings
        std::string LEFT_SIDE_VALUE=tokens[0];
        std::string RIGHT_SIDE_VALUE=tokens[2];

        //        std::cout<<"a - "<<LEFT_SIDE_VALUE<<std::endl;
        //        std::cout<<"b - "<<RIGHT_SIDE_VALUE<<std::endl;

        std::string LeftSideDecyption = GETPPESINGLE(LEFT_SIDE_VALUE ,KEY,Mode);
        std::string RightSideDecyption = GETPPESINGLE(RIGHT_SIDE_VALUE ,KEY,Mode);



        return RemoveTempsString(LeftSideDecyption)+""+RemoveTempsString(RightSideDecyption);
    }

}
//Get parallel processing function end


//Get Encyript start
std::string GET_ENCRYPT_PPE(std::string VALUE,std::string KEY,int Mode)
{

    if(Mode == 1)
    {
        std::string result = GETPPE(VALUE,KEY,Mode);
        return base64_encode(result);
    }
    else if(Mode == 0)
    {
        std::string Val = base64_decode_to_string(VALUE);

        std::string result = GETPPE(Val,KEY,Mode);
        return result;
    }

}
//Get Encryipt end


/********************PPE functions end**********************/



/********************main function start**********************/

int main()
{

    //Generate unixtime key test
    std::string timezone = "Asia/Tehran";
    std::string timeKey = GetCurrentTimeKey(timezone, false);
    std::cout << "Current Time Key: " << timeKey << "\n";
    std::cout << "Current Time Key: " << base64_encode(timeKey) << "\n";

    std::cout << "\n---------------------------------------------------\n";
    std::string EN = GETPPESINGLE("10,19;",timeKey,1);
    //std::string DE = GETPPESINGLE(EN,timeKey,0);

    copyToClipboard(EN);

    std::cout << "ENC : " << EN << "\n";

    std::string DE = GETPPESINGLE(EN,timeKey,0);
    std::cout << "DEC : " << DE << "\n";
    std::cout << "\n---------------------------------------------------\n";


    return 0;
}

/********************main function start**********************/