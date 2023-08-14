use std::collections::HashMap;
//use nitro_enclave_attestation_document::AttestationDocument;
//use std::fs::File;
use std::fs::{read, File};
//use std::io::Read;
use nitro_enclave_attestation_document::AttestationDocument;
use nsm_io::Request;
use nsm_io::Response;
use openssl::pkey::PKey;
use openssl::rsa::Rsa;
use serde::{Deserialize, Serialize};
use serde_bytes::ByteBuf;
use std::io::Write;
use std::str;
use std::vec::Vec;
use std::{fmt, fs};
use std::process;



fn generate_rsa_key() -> (ByteBuf, Vec<u8>) {
    let rsa = Rsa::generate(2048).unwrap();
    let pkey = PKey::from_rsa(rsa).unwrap();

    let pub_key: Vec<u8> = pkey.public_key_to_pem().unwrap();
    let private_key: Vec<u8> = pkey.private_key_to_pem_pkcs8().unwrap();
    let public_key = ByteBuf::from(pub_key);

    return (public_key, private_key);
}

fn main() {
    let nsm_fd = nsm_driver::nsm_init();
    let hello = ByteBuf::from("hello, world!");
    let nonce = ByteBuf::from("Nonce is here");
    let (public_key, private_key) = generate_rsa_key();
    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: Some(nonce),
    };
    let response: Response = nsm_driver::nsm_process_request(nsm_fd, request);
    if let Response::Attestation { ref document } = response {
        let response_bytes: &[u8] = &document.as_slice();
        if let Ok(mut file) = File::create("response.txt") {
            if let Err(err) = file.write_all(response_bytes) {
                eprintln!("Error writing to file: {}", err);
                process::exit(1);
            }
        } else {
            eprintln!("Error creating file");
            process::exit(1);
        }
    }




    // println!("{:?}", response.trim());

    nsm_driver::nsm_exit(nsm_fd);
}
