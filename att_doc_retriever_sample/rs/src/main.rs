use std::collections::HashMap;
//use nitro_enclave_attestation_document::AttestationDocument;
//use std::fs::File;
use std::fs::read;
//use std::io::Read;
use nsm_io::{Request};
use nsm_io::{Response};
use serde_bytes::ByteBuf;
use nitro_enclave_attestation_document::AttestationDocument;
use serde::{Serialize, Deserialize};
use std::fmt;

#[derive(Serialize, Deserialize)]
struct AttestationDocumentDecoded {
    pcrs: HashMap<String,String>,
    nonce: String,
    module_id: String,
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

    result = result.replace(&['[', ']', ',', ' '][..], "");

    result
}
fn main() {
    let nsm_fd = nsm_driver::nsm_init();

    let public_key = ByteBuf::from("my super secret key");
    let hello = ByteBuf::from("hello, world!");
    let nonce = ByteBuf::from("Nonce is here");

    let binding = read("/root/att_doc_retriever_sample/py/fake_cert.der").unwrap();
    let cert = binding.as_slice();

    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: Some(nonce),
    };


    let response = nsm_driver::nsm_process_request(nsm_fd, request);
    // println!("After request");

    if let Response::Attestation{ref document} = response {
        // println!("Test");
        // println!("{:?}", document);
        //let tester = AttestationDoc::from_binary(document.as_slice());
        let document_attested = match AttestationDocument::authenticate(document.as_slice(),cert) {
            Ok(doc) => {
                // signature of document authenticated and the data parsed correctly
                // println!("Success");
                doc
            },
            Err(err) => {
                // signature of document did not authenticate, or the data was poorly formed
                // Do something with the error here
                println!("{:?}", err);
                panic!("error unvalid atte doc");
            }
        };
        // println!("PCRS:");
        // println!("{:?}",document_attested.pcrs);
        let mut document_attested_decoded = AttestationDocumentDecoded {
            pcrs: HashMap::new(),
            nonce: String::new(),
            module_id: String::new(),
        };
        // println!("-----");
        for (index, pcr) in document_attested.pcrs.iter().enumerate(){
            let hex_vector = decimal_to_hex(&pcr);
            let result = remove_brackets_commas_and_spaces(&hex_vector);
            // println!("PCR{} value is: {:?}",index, result);
            // println!("-----");
            let pcr_index = format!("PCR{}",index);
            document_attested_decoded.pcrs.insert(pcr_index,result);
        }
        // println!("Module Id: {:?}",document_attested.module_id);

        document_attested_decoded.nonce = convert_decimals_to_ascii(document_attested.nonce);
        document_attested_decoded.module_id = document_attested.module_id;
        // println!("{}",document_attested_decoded);

        let json = serde_json::to_string(&document_attested_decoded).unwrap();
        println!("{}",json);


    }

    //let cose_struct = CoseSign1::new(&document, &Default::default(), &()).expect("TODO: panic message");


    /*let mut data_file = File::open("cert.der").unwrap();
    let mut trusted_root_certificate = String::new();
    data_file.read_to_string(&mut trusted_root_certificate).unwrap();
    println!(trusted_root_certificate);

    let document = match AttestationDocument::authenticate(&response, &trusted_root_certificate as &[u8]) {
  Ok(doc) => {
    // signature of document authenticated and the data parsed correctly
    doc
    },
  Err(err) => {
    // signature of document did not authenticate, or the data was poorly formed
    // Do something with the error here
    panic!("error");
  }
};*/
    // println!("After REsponse");

    // println!("{:?}", response);

    nsm_driver::nsm_exit(nsm_fd);
}


