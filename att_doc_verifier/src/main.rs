extern crate core;

use std::{fmt, str};
use std::collections::HashMap;
use std::fs::read;
use std::process::Command;
use nitro_enclave_attestation_document::AttestationDocument;
use serde::{Deserialize, Serialize};

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
        writeln!(f, "Module ID: {}", self.module_id)?;

        Ok(())
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
        .output()
        .expect("Failed to execute curl");

    let response_bytes: &[u8] = &output.stdout;
    let response_string = String::from_utf8_lossy(response_bytes);

    match serde_json::from_str::<Vec<u8>>(&response_string) {
        Ok(byte_vec) => {
            let att_document = AttestationDocument::authenticate(&byte_vec, cert);
            match att_document {
                Ok(doc) => {
                    let mut document_attested_decoded = AttestationDocumentDecoded {
                        pcrs: HashMap::new(),
                        nonce: String::new(),
                        module_id: String::new(),
                        public_key: String::new(),
                    };
                    for (index, pcr) in doc.pcrs.iter().enumerate() {
                        let hex_vector = pcr.iter().map(|&decimal| format!("{:02X}", decimal)).collect::<Vec<String>>().join("");
                        let pcr_index = format!("PCR{}", index);
                        document_attested_decoded.pcrs.insert(pcr_index, hex_vector);
                    }
                    document_attested_decoded.nonce = doc.nonce.map_or(String::new(), |v| String::from_utf8_lossy(&v).to_string());
                    document_attested_decoded.module_id = doc.module_id;
                    document_attested_decoded.public_key = doc.public_key.map_or(String::new(), |v| String::from_utf8_lossy(&v).to_string());
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
