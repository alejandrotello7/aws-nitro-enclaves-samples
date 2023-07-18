import ssl

def debug_certificate_paths():
    default_paths = ssl.get_default_verify_paths()
    print("Default Certificate Locations:")
    print("  - CA Certificates: ", default_paths.cafile)
    print("  - CA Certificate Directory: ", default_paths.capath)

debug_certificate_paths()