#include <iostream>
#include <string>
#include <ctime>
#include <vector>
#include <sstream>
#include <iomanip>

static const std::string base64_chars =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";

static const unsigned char b64_table[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";


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
    printf("Current GMT Unix time: %ld\n", (long)current_time);

    return (long)current_time;
}

std::string GetCurrentTimeKey(const std::string& Slat) {
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

    std::string encodedKey = base64_encode(Key);
    //std::cout << encodedKey;
    return encodedKey;
}

int main() {
    std::string timezone = "Asia/Tehran";
    std::string timeKey = GetCurrentTimeKey(timezone);
    std::cout << "Current Time Key: " << timeKey << std::endl;
    return 0;
}