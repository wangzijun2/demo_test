from tenanord.create_so_num_finsh import SoFinish

if __name__ == '__main__':
    so = SoFinish()
    so.update_so_dtl_qty()
    so.so_finish()
    so.select_next_receipt_num_id()
