extern crate core;

use std::{fmt, str};
use std::collections::HashMap;
use std::fs::read;
use std::process::Command;
use nitro_enclave_attestation_document::AttestationDocument;
use serde::{Deserialize, Serialize};
use serde_json::from_str;

#[derive(Serialize, Deserialize)]
struct AttestationDocumentDecoded {
    pcrs: HashMap<String, String>,
    nonce: String,
    module_id: String,
    public_key: String,
}

impl fmt::Display for AttestationDocumentDecoded {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "PCRData:")?;
        for (key, value) in &self.pcrs {
            writeln!(f, "PCR {}: {}", key, value)?;
        }
        writeln!(f, "Nonce: {}", self.nonce)?;
        writeln!(f, "Module ID: {}", self.module_id)
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
    vector.iter().map(|&decimal| format!("{:02X}", decimal)).collect()
}

fn remove_brackets_commas_and_spaces<T: std::fmt::Display>(vector: &[T]) -> String {
    let mut result = String::new();
    for (index, element) in vector.iter().enumerate() {
        result.push_str(&element.to_string());
        if index < vector.len() - 1 {
            result.push(' ');
        }
    }
    result.replace(&['[', ']', ',', ' '][..], "")
}

fn option_vec_u8_to_string(data: Option<Vec<u8>>) -> String {
    match data {
        Some(bytes) => String::from_utf8_lossy(&bytes).to_string(),
        None => String::new(),
    }
}

fn main() {
    let current_dir = std::env::current_dir().unwrap();
    let file_path = current_dir.join("cert.der");
    let binding = read(file_path).unwrap();
    let cert = binding.as_slice();
    let nonce_value = "nonce";

    let output = Command::new("curl")
        .arg("-X")
        .arg("GET")
        .arg(format!("https://ec2-3-70-6-196.eu-central-1.compute.amazonaws.com:5000/api/attestation_retriever/{}", nonce_value))
        .arg("--header")
        .arg("Content-Type: text/html")
        .arg("--data")
        .arg("@-")
        .arg("--silent")
        .arg("-o")
        .arg("/dev/stdout")
        .stdin(std::process::Stdio::piped())
        .output()
        .expect("Failed to execute curl");

    let response_bytes: &[u8] = &output.stdout;
    let response_string = String::from_utf8_lossy(response_bytes);
    let parsed: Result<Vec<u8>, serde_json::Error> = from_str(&response_string);

    match parsed {
        Ok(byte_vec) => {
            let byte_array: Vec<u8> = byte_vec.into_iter().take_while(|&x| x != 0).collect();
            let byte_slice = byte_array.as_slice();

            match AttestationDocument::authenticate(byte_slice, cert) {
                Ok(doc) => {
                    let mut document_attested_decoded = AttestationDocumentDecoded {
                        pcrs: HashMap::new(),
                        nonce: String::new(),
                        module_id: String::new(),
                        public_key: String::new(),
                    };
                    for (index, pcr) in doc.pcrs.iter().enumerate() {
                        let hex_vector = decimal_to_hex(&pcr);
                        let result = remove_brackets_commas_and_spaces(&hex_vector);
                        let pcr_index = format!("PCR{}", index);
                        document_attested_decoded.pcrs.insert(pcr_index, result);
                    }
                    document_attested_decoded.nonce = convert_decimals_to_ascii(doc.nonce);
                    document_attested_decoded.module_id = doc.module_id;
                    document_attested_decoded.public_key = option_vec_u8_to_string(doc.public_key);
                    let json = serde_json::to_string(&document_attested_decoded).unwrap();
                    println!("{}", json);
                },
                Err(err) => println!("Error: {}", err),
            }
        },
        Err(err) => println!("Error parsing JSON: {}", err),
    }
}
