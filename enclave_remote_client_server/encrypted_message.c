#include <openssl/pem.h>
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Function to convert hexadecimal string to byte array
int hex_to_bytes(const char *hex_str, unsigned char **bytes, size_t *bytes_len) {
    *bytes_len = strlen(hex_str) / 2;
    *bytes = (unsigned char *)malloc(*bytes_len);
    if (*bytes == NULL) return -1;

    for (size_t i = 0; i < *bytes_len; i++) {
        sscanf(&hex_str[i * 2], "%2hhx", &(*bytes)[i]);
    }
    return 0;
}

// Function to load RSA private key
RSA *load_private_key(const char *filename) {
    FILE *key_file = fopen(filename, "rb");
    if (!key_file) {
        perror("Unable to open file");
        return NULL;
    }
    RSA *rsa = RSA_new();
    rsa = PEM_read_RSAPrivateKey(key_file, &rsa, NULL, NULL);
    fclose(key_file);
    if (!rsa) {
        ERR_print_errors_fp(stderr);
    }
    return rsa;
}

// Function to decrypt message using RSA private key
int rsa_decrypt(RSA *rsa, const unsigned char *enc_data, size_t enc_data_len, unsigned char **decrypted) {
    if (!rsa || !enc_data) return -1;

    int padding = RSA_PKCS1_OAEP_PADDING;
    int rsa_size = RSA_size(rsa);
    *decrypted = (unsigned char *)malloc(rsa_size + 1);
    if (!*decrypted) return -1;

    int result = RSA_private_decrypt(enc_data_len, enc_data, *decrypted, rsa, padding);
    if (result == -1) {
        ERR_print_errors_fp(stderr);
        free(*decrypted);
        *decrypted = NULL;
    }
    return result;
}

int main() {
    const char *private_key_path = "private_key.pem";
    // Replace this with your actual hexadecimal encoded message
    const char *encoded_message_hex = "1344521e943dd997ef96941497ca630e6cfaad2cefff25855ed661388f245109cf23c4b0f7b15da6c3d800186ae9ab7c67fdaa54471335410c7cca4a9bfae8d224f9572fe67bb8b2ee7ad53bcce0b83e613897ac17f4cb04c04c7205d618881e2fe145d8747aa33b8307c5a554bf2b668c9b4c791b17dc2f9ee3acc44e0a46060ae8db3f8b867f4e26f5e6211a2bd3b01bf7253e612539187c7d218bb06d79abfd648f0ecbb4370228089da475ae8ea412e32063a3435d3eb2388bc103d47ca6270273cb4c07bbfdad85abb9769c8e1d4b4f4114faa6ec0f8f6768a52a4a6a549312f80b26cc509de16b59b7277df60dbe50d0597888742d452b0c21f3e6732b";
    unsigned char *encoded_message_bytes;
    size_t encoded_message_len;

    // Convert the encoded message from hexadecimal to bytes
    if (hex_to_bytes(encoded_message_hex, &encoded_message_bytes, &encoded_message_len) != 0) {
        fprintf(stderr, "Failed to convert hex to bytes\n");
        return 1;
    }

    // Load the private key
    RSA *rsa = load_private_key(private_key_path);
    if (!rsa) {
        fprintf(stderr, "Failed to load private key\n");
        free(encoded_message_bytes);
        return 2;
    }

    // Decrypt the message
    unsigned char *decrypted_message;
    int decrypted_message_len = rsa_decrypt(rsa, encoded_message_bytes, encoded_message_len, &decrypted_message);
    if (decrypted_message_len == -1) {
        fprintf(stderr, "Decryption failed\n");
        RSA_free(rsa);
        free(encoded_message_bytes);
        return 3;
    }

    // Print the decrypted message
    printf("Decrypted message: %.*s\n", decrypted_message_len, decrypted_message);

    // Cleanup
    RSA_free(rsa);
    free(encoded_message_bytes);
    free(decrypted_message);

    return 0;
}
