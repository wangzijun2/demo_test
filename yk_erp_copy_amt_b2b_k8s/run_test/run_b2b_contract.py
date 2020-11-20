from b2b_cust.create_contract import CreateContract

if __name__ == '__main__':
    c = CreateContract()
    c.save_contract()
    # c.zd_contract_audit()
    # c.yw_contract_audit()
    # c.cw_contract_audit()
    # c.create_contract_user()
