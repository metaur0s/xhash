
CURRENT_MODULE_ID = 0x10000

0bOOOXBBAA
  \\\ ||||____  8 OPCODES
      ||\\____      WHEN      | ORIG_SIZE | MODULE_ID | MODULE_NAME_LEN
      \\______      WHAT_SIZE | X_SIZE
           0bXX -> 0 A 4 -> 1 A 5

 64 0b01000000 0100BBAA  FILE   ======= ATE > 8GB DE ARQUIVOS
                     AA  LEN 1-4 BASE 1   ORIG_SIZE     
                   BB    LEN 1-4 BASE 1   X_SIZE
 80 0b01010000 0101BBAA  FILE   ======= ACIMA DE 8GB
                     AA  LEN 5-8 BASE 1   ORIG_SIZE     
                   BB    LEN 5-8 BASE 1   X_SIZE
    0bXXXXXXXX 1010XAAA  POSITION
                    AAA  LEN 1-8 BASE 0   POSITION
    0bXXXXXXXX 1011X---  RESERVED
    0bXXXXXXXX 11000AAA  CHECKSUM64
                    AAA  LEN 1-8 BASE 0   CHECKSUM
    0bXXXXXXXX 11001XXX  RESERVED
    0bXXXXXXXX 1101XXXX  RESERVED
    0bXXXXXXXX 1110XXXX  RESERVED
240 0b11110000 11110000  RESERVED
               1111....  RESERVED
               11111110  RESERVED
255 0b11111111 11111111  END

A BASE, PARA CADA WORD LENGTH
   ========        *     *   ====== NO CASO DO CSUM/POSITION, ESSA BASE AQUI É 0 E NÃO 1, POIS EXISTE SIM O 0
1               0x01  0x01      --->  POIS NAO EXISTE SIZE 0 - mas existe module_id 0 :S
2             0x0101  0x01 + 0x0100
3           0x010101  0x01 + 0x0100 + 0x010000
4         0x01010101  0x01 + 0x0100 + 0x010000 + 0x01000000
5       0x0101010101  0x01 + 0x0100 + 0x010000 + 0x01000000 + 0x0100000000
6     0x010101010101  0x01 + 0x0100 + 0x010000 + 0x01000000 + 0x0100000000 + 0x010000000000
7   0x01010101010101  0x01 + 0x0100 + 0x010000 + 0x01000000 + 0x0100000000 + 0x010000000000 + 0x01000000000000
8 0x0101010101010101  0x01 + 0x0100 + 0x010000 + 0x01000000 + 0x0100000000 + 0x010000000000 + 0x01000000000000 + 0x0100000000000000


0x0? ENTRY NULL
     ??   WHEN
     ??   WHAT_SIZE
     U8   WHAT[WHAT_SIZE]
0x1? ENTRY FILE
     U64  ORIG_HASH[2]
     ??   WHEN
     ??   WHAT_SIZE
     U8   WHAT[WHAT_SIZE]
0x2? FILE   (BELONGS TO CURRENT MODULE HASH TREE)
     U64  ORIG_HASH[2]
     ??   ORIG_SIZE
     ??   X_SIZE  <----     É ESTE VALOR  QUE TEM QUE SER USADO PARA IR SALTANDO   /   SE != ORIG_SIZE, ENTAO ESTÁ COMPRESSED
     U8   X[X_SIZE]
0x3? MODULE CHANGE
     ??   MODULE_ID
0x4? MODULE CREATE
     ??   MODULE_NAME_LEN
     CHAR MODULE_NAME[MODULE_NAME_LEN]
0x5? POSITION
0x6? CHECKSUM
     ??  CSUM <---- DESDE CSUM_START
0x7F END  <-- AO FECHAR TEM QUE ANTES COLOCAR O CHECKSUM SE POS != CSUM_START

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
