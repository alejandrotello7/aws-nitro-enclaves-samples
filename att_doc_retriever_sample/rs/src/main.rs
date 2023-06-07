//use nitro_enclave_attestation_document::AttestationDocument;
//use std::fs::File;
use std::fs::read;
//use std::io::Read;
use nsm_io::{Request};
use nsm_io::{Response};
use serde_bytes::ByteBuf;
use nitro_enclave_attestation_document::AttestationDocument;


fn main() {
    let nsm_fd = nsm_driver::nsm_init();

    let public_key = ByteBuf::from("my super secret key");
    let hello = ByteBuf::from("hello, world!");
    let nonce = ByteBuf::from("Nonce is here");

    let binding = read("/root/att_doc_retriever_sample/py/cert.der").unwrap();
    let cert = binding.as_slice();

    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: Some(nonce),
    };


    let response = nsm_driver::nsm_process_request(nsm_fd, request);
    println!("After request");

    if let Response::Attestation{ref document} = response {
        println!("Test");
        println!("{:?}", document);
        //let tester = AttestationDoc::from_binary(document.as_slice());
        let document_attested = match AttestationDocument::authenticate(document.as_slice(),cert) {
            Ok(doc) => {
                // signature of document authenticated and the data parsed correctly
                println!("Success");
                doc
            },
            Err(err) => {
                // signature of document did not authenticate, or the data was poorly formed
                // Do something with the error here
                println!("{:?}", err);
                panic!("error unvalid atte doc");
            }
        };
             println!("{:?}",document_attested.pcrs);
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
        println!("After REsponse");

        println!("{:?}", response);

        nsm_driver::nsm_exit(nsm_fd);
    }
