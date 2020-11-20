# from mdm.create_protocol_item import CreateProtocolItem
from mdm.create_protocal_item import CreateProtocolItem

# 创建新建商品
if __name__ == "__main__":
    create = CreateProtocolItem()
    create.save_supply_hdr()
    create.save_supply_dtl()
    # create.add_sub_unit()
    # create.zd_audit()
    # create.yw_audit()
    # create.cw_audit()
