#include <openssl/pem.h>
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to load the RSA private key
RSA *load_private_key(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Unable to open private key file");
        return NULL;
    }
    RSA *rsa = PEM_read_RSAPrivateKey(fp, NULL, NULL, NULL);
    fclose(fp);
    if (rsa == NULL) {
        ERR_print_errors_fp(stderr);
    }
    return rsa;
}

// Function to decrypt the message
int decrypt_message(RSA *rsa, const unsigned char *enc_data, size_t enc_data_len, unsigned char **decrypted) {
    if (rsa == NULL || enc_data == NULL) return -1;

    int padding = RSA_PKCS1_OAEP_PADDING;
    int rsa_size = RSA_size(rsa);
    *decrypted = (unsigned char*)malloc(rsa_size + 1);

    int result = RSA_private_decrypt(enc_data_len, enc_data, *decrypted, rsa, padding);
    if (result == -1) {
        ERR_print_errors_fp(stderr);
        free(*decrypted);
        *decrypted = NULL;
    }
    return result;
}

// Function to convert Base64 encoded data to binary. Placeholder for actual function.
// You'll need to implement or use a library function for actual Base64 decoding.
size_t base64_decode(const char *base64_data, unsigned char **decoded_data) {
    // Placeholder: Implement Base64 decoding or use a library like OpenSSL's EVP_DecodeBlock
    return 0; // Return the length of decoded data
}

int main() {
    const char *private_key_path = "private_key.pem";
    const char *encrypted_base64 = "cqBXkNgd7zdk0LsrFRJXipYcq6GPyPyQCQhn+oR0MjmYwWqhzackqMOyO6+eecRBo0cqC2Kp14IqmtlVyKRz8dH/e3dIYFLeN3ZEVoFb9q1bAPo66Mwcb8g5lQy4d8Mjs9eGF+ESLxU5mhvyyMQ0/0y5kkgEkqILa3FTYUUebnoc2sT9lPuJ6tsBSiUsIbGAxiZuoR1atW85yWDyVFV+d+RFxM6KDQwZPunB59GKrdd4A9+YwBL5b0ACyzU3oJTCk/KZhKIE4jxRgRfjGJ99F1jpxcvFzyvLtZCznO/R1dKQtcYvvOXAkSor1/dEo/i/eQJVTxuGB3jJIbosF/QAMQ==";
    unsigned char *encrypted_data;
    unsigned char *decrypted_data;
    size_t encrypted_data_len;

    // Load RSA private key
    RSA *rsa = load_private_key(private_key_path);
    if (rsa == NULL) {
        fprintf(stderr, "Failed to load private key\n");
        return 1;
    }

    // Decode the Base64 encoded encrypted message
    encrypted_data_len = base64_decode(encrypted_base64, &encrypted_data);

    // Decrypt the message
    int decrypted_data_len = decrypt_message(rsa, encrypted_data, encrypted_data_len, &decrypted_data);
    if (decrypted_data_len == -1) {
        fprintf(stderr, "Decryption failed\n");
        RSA_free(rsa);
        free(encrypted_data);
        return 2;
    }

    // Print the decrypted message
    printf("Decrypted message: %.*s\n", decrypted_data_len, decrypted_data);

    // Cleanup
    RSA_free(rsa);
    free(encrypted_data);
    free(decrypted_data);

    return 0;
}
