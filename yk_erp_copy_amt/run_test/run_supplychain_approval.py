from supplychain.create_approval import CreateApproval

if __name__ == "__main__":
    c = CreateApproval()
    c.write_approval_reserved()
    c.create_approval_hdr()
    c.save_approval_dtl()
    # c.approval_audit()