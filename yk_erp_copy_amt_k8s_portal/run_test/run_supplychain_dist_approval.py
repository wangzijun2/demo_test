from supplychain.create_dist_approval import CreateDistApproval

if __name__ == "__main__":
    c = CreateDistApproval()
    c.create_dist_approval_hdr()
    c.create_dist_approval_dtl()
    # c.dist_approval_audit()
    # c.write_so_num_ids()

