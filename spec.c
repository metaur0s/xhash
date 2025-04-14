
CURRENT_MODULE_ID = 0x10000

0x00 ENTRY NULL
     U32 WHEN
     U16 WHAT_SIZE
     U8  WHAT[WHAT_SIZE]
0x01 ENTRY FILE
     U64 ORIG_HASH[2]
     U32 WHEN
     U16 WHAT_SIZE
     U8  WHAT[WHAT_SIZE]
0x02 FILE   (BELONGS TO CURRENT MODULE HASH TREE)
     U64 ORIG_HASH[2]
     U64 ORIG_SIZE
     U64 X_SIZE  <----     É ESTE VALOR  QUE TEM QUE SER USADO PARA IR SALTANDO   /   SE != ORIG_SIZE, ENTAO ESTÁ COMPRESSED
     U8  X[X_SIZE]
0x03 MODULE CHANGE
     U16  MODULE_ID
0x04 MODULE CREATE
     U8   MODULE_NAME_LEN
     CHAR MODULE_NAME[MODULE_NAME_LEN]
0x05 CHECKSUM
     U64 CSUM <---- DESDE CSUM_START
0x06 END

struct ctx_s {
 // O PYTHON LE DAQUI USANDO O INT.FROM_BYTES()
    u64 orig_hash[2];
    u64 when;
    u64 size; // what | orig | module_name
    u64 x_size;
    u64 pos; // what | x | module_name
    u64 reserved[2];
// -----
    int fd;
    uint cur_mod;
    u64 csum;
    void* csum_start;
    void* pos;
    void* end;
    char fpath[512];
};

match c_function_read_at_opcode(self.cctx):
   case ENTRY_NULL:
       when
       what_size
       what_pos
   case ENTRY_FILE:
       orig_hash[2]
       when
       what_size
       what_pos
   case FILE:
       orig_hash[2]
       orig_size
       x_size
       x_pos
       assert 1 <= x_size <= orig_size
    # NORMALMENTE SÓ ESTAMOS REGSTRANDO AS COISAS NO NOSSO DICT
    # ISSO AQUI É SÓ SE QUISERMOS LER O CONTEUDO
       if x_size != orig_size:
           x = decompress(x, orig_size)
   case MODULE_CHANGE:
        module_id
     assert module_id < len(mods)
     mod_current = module_id
   case MODULE_CREATE:
        module_name_len
        module_name_pos
     assert ((mod_current < len(mods)) or 
             (mod_current == 0x10000 and len(mods) == 0))
     mod_current = len(mods)
     modNames.append(str.decode(buff[module_name_pos:module_name_pos+module_name_len]))
   case END:
        pass
   case _:
        raise ValueError
