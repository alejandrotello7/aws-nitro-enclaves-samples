use std::collections::HashMap;
use std::fs::{read};
use nitro_enclave_attestation_document::AttestationDocument;
use nsm_io::Response;
use serde::{Deserialize, Serialize};
use std::str;
use std::process::Command;
use serde_json::from_str;


#[derive(Serialize, Deserialize)]
struct AttestationDocumentDecoded {
    pcrs: HashMap<String, String>,
    nonce: String,
    module_id: String,
    public_key: String,
}
fn main() {
    let current_dir = std::env::current_dir().unwrap();
    let file_path = current_dir.join("cert.der");
    let binding = read(file_path).unwrap();
    let cert = binding.as_slice();

    let output = Command::new("curl")
        .arg("-X")
        .arg("GET")
        .arg("https://ec2-18-159-253-51.eu-central-1.compute.amazonaws.com:5000/api/attestation_retriever")
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

    let response = String::from_utf8_lossy(&output.stdout).to_string();
    let response_bytes: &[u8] = response.trim().as_bytes();
    let attestation_response: Result<Response,_> = from_str(&response);

    let _document = match AttestationDocument::authenticate(&response_bytes, cert){
        Ok(_doc) => {
            println!("Correct");
        },
        Err(err) => {
            println!("Error: {}", err);
        }
    };

    // if let Ok(Response::Attestation { ref document }) = attestation_response {
    //     let document_attested = match AttestationDocument::authenticate(document.as_slice(), cert) {
    //         Ok(doc) => doc,
    //         Err(err) => {
    //             println!("{:?}", err);
    //             panic!("error invalid attestation document");
    //         }
    //     };
    //     println!("Correct!");
    //     let mut document_attested_decoded = AttestationDocumentDecoded {
    //         pcrs: HashMap::new(),
    //         nonce: String::new(),
    //         module_id: String::new(),
    //         public_key: String::new(),
    //     };
    //     // println!("-----");
    //     for (index, pcr) in document_attested.pcrs.iter().enumerate() {
    //         let hex_vector = decimal_to_hex(&pcr);
    //         let result = remove_brackets_commas_and_spaces(&hex_vector);
    //         // println!("PCR{} value is: {:?}",index, result);
    //         // println!("-----");
    //         let pcr_index = format!("PCR{}", index);
    //         document_attested_decoded.pcrs.insert(pcr_index, result);
    //     }
    //     // println!("Module Id: {:?}",document_attested.module_id);
    //
    //     document_attested_decoded.nonce = convert_decimals_to_ascii(document_attested.nonce);
    //     document_attested_decoded.module_id = document_attested.module_id;
    //     document_attested_decoded.public_key =
    //         option_vec_u8_to_string(document_attested.public_key);
    //
    //     // println!("{}",document_attested_decoded);
    //
    //     let json = serde_json::to_string(&document_attested_decoded).unwrap();
    //     println!("{}", json);
    // }
    // else if let Err(err) = attestation_response {
    //     println!("Error parsing response: {:?}", err);
    //     println!("Failed");
    // }






}
