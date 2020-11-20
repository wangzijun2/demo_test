from logistics.receipt_bud_hdr import SelectReceiptHdr

if __name__ == "__main__":
    receipt = SelectReceiptHdr()
    receipt.update_item_num_qty()
    receipt.receipt_finish()