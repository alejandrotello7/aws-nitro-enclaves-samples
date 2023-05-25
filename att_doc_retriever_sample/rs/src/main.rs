//use std::fs::File;
//use std::io::Read;
use nsm_io::Request;
use serde_bytes::ByteBuf;
//use nitro_enclave_attestation_document::AttestationDocument;


fn main() {
    let nsm_fd = nsm_driver::nsm_init();

    let public_key = ByteBuf::from("my super secret key");
    let hello = ByteBuf::from("hello, world!");

    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: None,
    };

    let response = nsm_driver::nsm_process_request(nsm_fd, request);
    println!("{:?}", response);

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

    nsm_driver::nsm_exit(nsm_fd);
}
