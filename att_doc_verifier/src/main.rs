extern crate core;

use std::{fmt, str};
use std::collections::HashMap;
use std::fs::{read };
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
fn main() {
    let current_dir = std::env::current_dir().unwrap();
    let file_path = current_dir.join("cert.der");
    let binding = read(file_path).unwrap();
    let cert = binding.as_slice();

    let output = Command::new("curl")
        .arg("-X")
        .arg("GET")
        .arg("https://ec2-18-156-193-73.eu-central-1.compute.amazonaws.com:5000/api/attestation_retriever")
        .arg("--header")
        .arg("Content-Type: text/html")
        .arg("--data")
        .arg("@-")  //
        .arg("--silent")  // Suppress progress meter
        .arg("-o")
        .arg("/dev/stdout")  // Output to stdout
        .stdin(std::process::Stdio::piped())
        .output()
        .expect("Failed to execute curl");

    let response_bytes: &[u8] = &output.stdout;
    let response_string = String::from_utf8_lossy(response_bytes);
    let parsed: Result<Vec<u8>, serde_json::Error> = from_str(&response_string);
    match parsed {
        Ok(byte_vec) => {
            const SIZE: usize = 4900; // Change this to the desired size
            let mut byte_array: [u8; SIZE] = [0; SIZE];

            for i in 0..SIZE {
                byte_array[i] = byte_vec[i];
            }
            // println!("{:?}", byte_array);
            let _document_attested = match AttestationDocument::authenticate(&byte_array, cert){
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
                    document_attested_decoded.public_key =
                        option_vec_u8_to_string(doc.public_key);
                    let json = serde_json::to_string(&document_attested_decoded).unwrap();
                    println!("{}", json);

                },
                Err(err) => {
                    println!("Error: {}", err);
                }
            };

        }
        Err(err) => {
            println!("Error parsing JSON: {}", err);
        }
    }


}
