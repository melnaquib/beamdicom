from pynetdicom3 import AE

# The Verification SOP Class has a UID of 1.2.840.10008.1.1
ae = AE(scu_sop_class=['1.2.840.10008.1.1'])

# Try and associate with the peer AE
#   Returns the Association thread
print('Requesting Association with the peer')
assoc = ae.associate("localhost", 7000)

if assoc.is_established:
    print('Association accepted by the peer')
    # Send a DIMSE C-ECHO request to the peer
    assoc.send_c_echo()

    # Release the association
    assoc.release()
elif assoc.is_rejected:
    print('Association was rejected by the peer')
elif assoc.is_aborted:
    print('Received an A-ABORT from the peer during Association')