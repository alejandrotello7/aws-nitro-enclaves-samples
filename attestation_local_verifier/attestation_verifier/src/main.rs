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

#[derive(Serialize, Deserialize)]
struct AttestationDocumentDecoded {
    pcrs: HashMap<String, String>,
    nonce: String,
    module_id: String,
    public_key: String,
    private_key_path: String,
    public_key_path: String,
}
impl fmt::Display for AttestationDocumentDecoded {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "PCRData:")?;
        writeln!(f, "PCR Values:")?;
        for (key, value) in &self.pcrs {
            writeln!(f, "PCR {}: {}", key, value)?;
        }
        writeln!(f, "Nonce: {}", self.nonce)?;
        writeln!(f, "Module ID: {}", self.module_id)?;

        Ok(())
    }
}
fn convert_decimals_to_ascii(input: Option<Vec<u8>>) -> String {
    if let Some(decimals) = input {
        let mut result = String::new();

        for decimal in decimals {
            result.push(decimal as char);
        }

        return result;
    }

    String::new()
}
fn decimal_to_hex(vector: &[u8]) -> Vec<String> {
    vector
        .iter()
        .map(|&decimal| format!("{:02X}", decimal))
        .collect()
}
fn remove_brackets_commas_and_spaces<T: std::fmt::Display>(vector: &[T]) -> String {
    let mut result = String::new();

    for (index, element) in vector.iter().enumerate() {
        result.push_str(&element.to_string());

        if index < vector.len() - 1 {
            result.push(' ');
        }
    }

    result = result.replace(&['[', ']', ',', ' '][..], "");

    result
}
fn option_vec_u8_to_string(data: Option<Vec<u8>>) -> String {
    match data {
        Some(bytes) => String::from_utf8_lossy(&bytes).to_string(),
        None => String::new(),
    }
}
fn generate_rsa_key() -> (ByteBuf, Vec<u8>) {
    let rsa = Rsa::generate(2048).unwrap();
    let pkey = PKey::from_rsa(rsa).unwrap();

    let pub_key: Vec<u8> = pkey.public_key_to_pem().unwrap();
    let private_key: Vec<u8> = pkey.private_key_to_pem_pkcs8().unwrap();
    let public_key = ByteBuf::from(pub_key);

    return (public_key, private_key);
}

fn main() {

    let current_dir = std::env::current_dir().unwrap();
    let file_path = current_dir.join("cert.der");
    let binding = fs::read(file_path).unwrap();

    let cert = binding.as_slice();

    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: Some(nonce),
    };

    let response = nsm_driver::nsm_process_request(nsm_fd, request);

    if let Response::Attestation { ref document } = response {
        let document_attested = match AttestationDocument::authenticate(document.as_slice(), cert) {
            Ok(doc) => doc,
            Err(err) => {
                println!("{:?}", err);
                panic!("error unvalid atte doc");
            }
        };
        let mut document_attested_decoded = AttestationDocumentDecoded {
            pcrs: HashMap::new(),
            nonce: String::new(),
            module_id: String::new(),
            public_key: String::new(),
            private_key_path: String::new(),
            public_key_path: String::new(),
        };
        // println!("-----");
        for (index, pcr) in document_attested.pcrs.iter().enumerate() {
            let hex_vector = decimal_to_hex(&pcr);
            let result = remove_brackets_commas_and_spaces(&hex_vector);
            // println!("PCR{} value is: {:?}",index, result);
            // println!("-----");
            let pcr_index = format!("PCR{}", index);
            document_attested_decoded.pcrs.insert(pcr_index, result);
        }
        // println!("Module Id: {:?}",document_attested.module_id);

        document_attested_decoded.nonce = convert_decimals_to_ascii(document_attested.nonce);
        document_attested_decoded.module_id = document_attested.module_id;
        document_attested_decoded.public_key =
            option_vec_u8_to_string(document_attested.public_key);
        document_attested_decoded.private_key_path = private_key_path.parse().unwrap();
        document_attested_decoded.public_key_path = public_key_path.parse().unwrap();

        // println!("{}",document_attested_decoded);

        let json = serde_json::to_string(&document_attested_decoded).unwrap();
        println!("{}", json);
    }

    nsm_driver::nsm_exit(nsm_fd);
}
