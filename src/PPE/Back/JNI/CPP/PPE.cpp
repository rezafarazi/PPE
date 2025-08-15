#include "include/jni.h"
#include <string>
#include <vector>

extern "C" {

/********************JNI functions start**********************/

jstring stringToJString(JNIEnv* env, const std::string& str) {
    return env->NewStringUTF(str.c_str());
}

std::string jStringToString(JNIEnv* env, jstring jStr) {
    if (!jStr) return "";

    const char *chars = env->GetStringUTFChars(jStr, NULL);
    std::string str(chars);
    env->ReleaseStringUTFChars(jStr, chars);

    return str;
}

/********************JNI functions end**********************/

JNIEXPORT jstring JNICALL Java_PPE_GetEncrypt(JNIEnv *env, jobject obj, jstring VALUE) {
    return stringToJString(env, "Hello reza");
}

JNIEXPORT jstring JNICALL Java_PPE_GetDecrypt(JNIEnv *env, jobject obj, jstring VALUE) {
    return stringToJString(env, "Hello I am fine");
}

}
