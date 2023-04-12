# This script takes a path of folder containing diff files generated by designite_diff script.
# It assumes that the file names are in <project>.<commit-hash1>.<commit-hash2> format.
import os
import sys
from constants import *


def _get_smell_type(line):
    if line.startswith('New Architecture smells:'):
        return SmellType.ARCH, OperationType.New
    if line.startswith('Removed Architecture smells:'):
        return SmellType.ARCH, OperationType.Removed
    if line.startswith('Modified Architecture smells:'):
        return SmellType.ARCH, OperationType.Modified

    if line.startswith('New Design smells:'):
        return SmellType.DESIGN, OperationType.New
    if line.startswith('Removed Design smells:'):
        return SmellType.DESIGN, OperationType.Removed
    if line.startswith('Modified Design smells:'):
        return SmellType.DESIGN, OperationType.Modified

    if line.startswith('New Implementation smells:'):
        return SmellType.IMPL, OperationType.New
    if line.startswith('Removed Implementation smells:'):
        return SmellType.IMPL, OperationType.Removed
    if line.startswith('Modified Implementation smells:'):
        return SmellType.IMPL, OperationType.Modified
    return None, None


class SmellType:
    ARCH = 0
    DESIGN = 1
    IMPL = 2

class OperationType:
    New = 0
    Modified = 1
    Removed = 2

class ArchSmellCount:
    def __init__(self):
        self.cyc_dep = 0
        self.amb_int = 0
        self.fea_con = 0
        self.uns_dep = 0
        self.den_str = 0
        self.sca_fun = 0
        self.god_com = 0

    def total(self):
        return self.cyc_dep + self.amb_int + self.fea_con + self.uns_dep + self.den_str + self.sca_fun + self.god_com

    def count(self, line):
        smell_name = line.split(',')[2].strip()
        if smell_name == A_AMB_INT:
            self.amb_int += 1
        elif smell_name == A_FEA_CON:
            self.fea_con += 1
        elif smell_name == A_UNS_DEP:
            self.uns_dep += 1
        elif smell_name == A_CYC_DEP:
            self.cyc_dep += 1
        elif smell_name == A_DEN_STR:
            self.den_str += 1
        elif smell_name == A_SCA_FUN:
            self.sca_fun += 1
        elif smell_name == A_GOD_COM:
            self.god_com += 1

    def __str__(self):
        return str(self.amb_int) + ',' + str(self.fea_con) + ',' + str(
            self.uns_dep) + ',' + str(self.cyc_dep) + ',' + str(self.den_str) + ',' + str(
            self.sca_fun) + ',' + str(self.god_com)

class DesignSmellCount:
    def __init__(self):
        self.unn_abs = 0
        self.imp_abs = 0
        self.mul_abs = 0
        self.unut_abs = 0
        self.dup_abs = 0
        self.fea_env = 0
        self.def_enc = 0
        self.uxp_enc = 0
        self.bro_mod = 0
        self.ins_mod = 0
        self.hub_mod = 0
        self.cyc_mod = 0
        self.wid_hie = 0
        self.dee_hie = 0
        self.mul_hie = 0
        self.cyc_hie = 0
        self.reb_hie = 0
        self.unf_hie = 0
        self.mis_hie = 0
        self.bro_hie = 0

    def total(self):
        return self.unn_abs + self.imp_abs + self.mul_abs + self.unut_abs + self.dup_abs + self.fea_env + self.def_enc + self.uxp_enc + self.bro_mod + self.ins_mod + self.hub_mod + self.cyc_mod + self.wid_hie + self.dee_hie + self.mul_hie + self.cyc_hie + self.reb_hie + self.unf_hie + self.mis_hie + self.bro_hie

    def count(self, line):
        smell_name = line.split(',')[3].strip()
        if smell_name == D_UNN_ABS:
            self.unn_abs += 1
        elif smell_name == D_IMP_ABS:
            self.imp_abs += 1
        elif smell_name == D_MUL_ABS:
            self.mul_abs += 1
        elif smell_name == D_UNUT_ABS:
            self.unut_abs += 1
        elif smell_name == D_DUP_ABS:
            self.dup_abs += 1
        elif smell_name == D_FEA_ENV:
            self.fea_env += 1
        elif smell_name == D_DEF_ENC:
            self.def_enc += 1
        elif smell_name == D_UXP_ENC:
            self.uxp_enc += 1
        elif smell_name == D_BRO_MOD:
            self.bro_mod += 1
        elif smell_name == D_INS_MOD:
            self.ins_mod += 1
        elif smell_name == D_HUB_MOD:
            self.hub_mod += 1
        elif smell_name == D_CYC_MOD:
            self.cyc_mod += 1
        elif smell_name == D_WID_HIE:
            self.wid_hie += 1
        elif smell_name == D_DEE_HIE:
            self.dee_hie += 1
        elif smell_name == D_MUL_HIE:
            self.mul_hie += 1
        elif smell_name == D_CYC_HIE:
            self.cyc_hie += 1
        elif smell_name == D_REB_HIE:
            self.reb_hie += 1
        elif smell_name == D_UNF_HIE:
            self.unf_hie += 1
        elif smell_name == D_MIS_HIE:
            self.mis_hie += 1
        elif smell_name == D_BRO_HIE:
            self.bro_hie += 1

    def __str__(self):
        return str(self.unn_abs) + ',' + str(
            self.imp_abs) + ',' + str(self.mul_abs) + ',' + str(
            self.unut_abs) + ',' + str(self.dup_abs) + ',' + str(
            self.fea_env) + ',' + str(self.def_enc) + ',' + str(
            self.uxp_enc) + ',' + str(self.bro_mod) + ',' + str(
            self.ins_mod) + ',' + str(self.hub_mod) + ',' + str(
            self.cyc_mod) + ',' + str(self.wid_hie) + ',' + str(
            self.dee_hie) + ',' + str(self.mul_hie) + ',' + str(
            self.cyc_hie) + ',' + str(self.reb_hie) + ',' + str(
            self.unf_hie) + ',' + str(self.mis_hie) + ',' + str(
            self.bro_hie)

class ImplSmellCount:
    def __init__(self):
        self.long_mth = 0
        self.comp_mth = 0
        self.long_param_list = 0
        self.long_id = 0
        self.long_stmt = 0
        self.comp_cond = 0
        self.virtual_call = 0
        self.emty_catch = 0
        self.magic_no = 0
        self.dup_code = 0
        self.mis_def = 0

    def total(self):
        return self.long_mth + self.comp_mth + self.long_param_list + self.long_id + self.long_stmt + self.comp_cond + self.virtual_call + self.emty_catch + self.magic_no + self.dup_code + self.mis_def

    def count(self, line):
        tokens = line.split(',')
        if len(tokens) < 5:
            return
        smell_name = tokens[4].strip()
        if smell_name == I_LONG_MTD:
            self.long_mth += 1
        elif smell_name == I_COMP_MTD:
            self.comp_mth += 1
        elif smell_name == I_LONG_PARAM_LIST:
            self.long_param_list += 1
        elif smell_name == I_LONG_ID:
            self.long_id += 1
        elif smell_name == I_LONG_STMT:
            self.long_stmt += 1
        elif smell_name == I_COMP_COND:
            self.comp_cond += 1
        elif smell_name == I_VIRTUAL_CALL:
            self.virtual_call += 1
        elif smell_name == I_EMTY_CATCH:
            self.emty_catch += 1
        elif smell_name == I_MAGIC_NO:
            self.magic_no += 1
        elif smell_name == I_DUP_CODE:
            self.dup_code += 1
        elif smell_name == I_MIS_DEF:
            self.mis_def += 1

    def __str__(self):
        return str(self.long_mth) + ',' + str(self.comp_mth) + ',' + str(
            self.long_param_list) + ',' + str(self.long_id) + ',' + str(
            self.long_stmt) + ',' + str(self.comp_cond) + ',' + str(
            self.virtual_call) + ',' + str(self.emty_catch) + ',' + str(
            self.magic_no) + ',' + str(self.dup_code) + ',' + str(self.mis_def)


def _get_active_hash(line, hash1, hash2):
    if line.strip().endswith(hash1):
        return hash1
    if line.strip().endswith(hash2):
        return hash2
    print('Error state: hash must be one of the commit hashes')
    return None


def _write_to_csv(out_file, hash1, hash2, new_arch_smells, mod_arch_smells, rem_arch_smells, new_design_smells, mod_design_smells, rem_design_smells, new_impl_smells, mod_impl_smells, rem_impl_smells):
    total_new = new_arch_smells.total() + new_design_smells.total() + new_impl_smells.total()
    total_mod = mod_arch_smells.total() + mod_design_smells.total() + mod_impl_smells.total()
    total_rem = rem_arch_smells.total() + rem_design_smells.total() + rem_impl_smells.total()
    line = hash1 + ',' + hash2 + ',' + str(new_arch_smells) + ',' + str(mod_arch_smells) + ',' + str(rem_arch_smells) + ',' + str(new_design_smells) + ',' + str(mod_design_smells) + ',' + str(rem_design_smells) + ',' + str(new_impl_smells) + ',' + str(mod_impl_smells) + ',' + str(rem_impl_smells) + ',' +str(new_arch_smells.total()) + ',' + str(mod_arch_smells.total()) + ',' + str(rem_arch_smells.total()) + ',' + str(new_design_smells.total()) + ',' + str(mod_design_smells.total()) + ',' + str(rem_design_smells.total()) + ',' + str(new_impl_smells.total()) + ',' + str(mod_impl_smells.total()) + ',' + str(rem_impl_smells.total()) + ',' + str(total_new) + ',' + str(total_mod) + ',' + str(total_rem) +'\n'
    out_file.write(line)


def compare_quantify(folder_path):
    with open('compare_quantify.csv', 'w') as out_file:
        out_file.write(
            'hash1,hash2,' +
            'New_A_AMB_INT,New_A_FEA_CON,New_A_UNS_DEP,New_A_CYC_DEP,New_A_DEN_STR,New_A_SCA_FUN,New_A_GOD_COM,Mod_A_AMB_INT,' +
            'Mod_A_FEA_CON,Mod_A_UNS_DEP,Mod_A_CYC_DEP,Mod_A_DEN_STR,Mod_A_SCA_FUN,Mod_A_GOD_COM,' +
            'Rem_A_AMB_INT,Rem_A_FEA_CON,Rem_A_UNS_DEP,Rem_A_CYC_DEP,Rem_A_DEN_STR,Rem_A_SCA_FUN,Rem_A_GOD_COM,' +
            'New_D_UNN_ABS,New_D_IMP_ABS,New_D_MUL_ABS,New_D_UNUT_ABS,New_D_DUP_ABS,New_D_FEA_ENV,New_D_DEF_ENC,New_D_UXP_ENC,New_D_BRO_MOD,New_D_INS_MOD,New_D_HUB_MOD,New_D_CYC_MOD,New_D_WID_HIE,New_D_DEE_HIE,New_D_MUL_HIE,New_D_CYC_HIE,New_D_REB_HIE,New_D_UNF_HIE,New_D_MIS_HIE,New_D_BRO_HIE,' +
            'Mod_D_UNN_ABS,Mod_D_IMP_ABS,Mod_D_MUL_ABS,Mod_D_UNUT_ABS,Mod_D_DUP_ABS,Mod_D_FEA_ENV,Mod_D_DEF_ENC,Mod_D_UXP_ENC,Mod_D_BRO_MOD,Mod_D_INS_MOD,Mod_D_HUB_MOD,Mod_D_CYC_MOD,Mod_D_WID_HIE,Mod_D_DEE_HIE,Mod_D_MUL_HIE,Mod_D_CYC_HIE,Mod_D_REB_HIE,Mod_D_UNF_HIE,Mod_D_MIS_HIE,Mod_D_BRO_HIE,' +
            'Rem_D_UNN_ABS,Rem_D_IMP_ABS,Rem_D_MUL_ABS,Rem_D_UNUT_ABS,Rem_D_DUP_ABS,Rem_D_FEA_ENV,Rem_D_DEF_ENC,Rem_D_UXP_ENC,Rem_D_BRO_MOD,Rem_D_INS_MOD,Rem_D_HUB_MOD,Rem_D_CYC_MOD,Rem_D_WID_HIE,Rem_D_DEE_HIE,Rem_D_MUL_HIE,Rem_D_CYC_HIE,Rem_D_REB_HIE,Rem_D_UNF_HIE,Rem_D_MIS_HIE,Rem_D_BRO_HIE,' +
            'New_I_LONG_MTD,New_I_COMP_MTD,New_I_LONG_PARAM_LIST,New_I_LONG_ID,New_I_LONG_STMT,New_I_COMP_COND,New_I_VIRTUAL_CALL,New_I_EMTY_CATCH,New_I_MAGIC_NO,New_I_DUP_CODE,New_I_MIS_DEF,' +
            'Mod_I_LONG_MTD,Mod_I_COMP_MTD,Mod_I_LONG_PARAM_LIST,Mod_I_LONG_ID,Mod_I_LONG_STMT,Mod_I_COMP_COND,Mod_I_VIRTUAL_CALL,Mod_I_EMTY_CATCH,Mod_I_MAGIC_NO,Mod_I_DUP_CODE,Mod_I_MIS_DEF,' +
            'Rem_I_LONG_MTD,Rem_I_COMP_MTD,Rem_I_LONG_PARAM_LIST,Rem_I_LONG_ID,Rem_I_LONG_STMT,Rem_I_COMP_COND,Rem_I_VIRTUAL_CALL,Rem_I_EMTY_CATCH,Rem_I_MAGIC_NO,Rem_I_DUP_CODE,Rem_I_MIS_DEF,' +
            'Total_new_arch,Total_mod_arch,Total_rem_arch,Total_new_design,Total_mod_design,Total_rem_design,Total_new_impl,Total_mod_impl,Total_rem_impl,Total_New,Total_Mod,Total_Rem\n')
        for file in os.listdir(folder_path):
            tokens = file.split('.')
            if len(tokens) == 4:
                hash1 = tokens[2]
                hash2 = tokens[3]
                with open(os.path.join(folder_path, file)) as file_obj:
                    smell_type = SmellType.ARCH
                    op_type = OperationType.New
                    new_arch_smells = ArchSmellCount()
                    mod_arch_smells = ArchSmellCount()
                    rem_arch_smells = ArchSmellCount()
                    new_design_smells = DesignSmellCount()
                    mod_design_smells = DesignSmellCount()
                    rem_design_smells = DesignSmellCount()
                    new_impl_smells = ImplSmellCount()
                    mod_impl_smells = ImplSmellCount()
                    rem_impl_smells = ImplSmellCount()

                    for line in file_obj:
                        cur_smell_type, cur_op_type = _get_smell_type(line)
                        if cur_smell_type is not None:
                            smell_type = cur_smell_type
                            op_type = cur_op_type
                            continue

                        if smell_type == SmellType.ARCH:
                            if op_type == OperationType.New:
                                new_arch_smells.count(line)
                            elif op_type  == OperationType.Modified:
                                mod_arch_smells.count(line)
                            else:
                                rem_arch_smells.count(line)
                        elif smell_type == SmellType.DESIGN:
                            if op_type == OperationType.New:
                                new_design_smells.count(line)
                            elif op_type  == OperationType.Modified:
                                mod_design_smells.count(line)
                            else:
                                rem_design_smells.count(line)
                        elif smell_type == SmellType.IMPL:
                            if op_type == OperationType.New:
                                new_impl_smells.count(line)
                            elif op_type  == OperationType.Modified:
                                mod_impl_smells.count(line)
                            else:
                                rem_impl_smells.count(line)
                    _write_to_csv(out_file, hash1, hash2, new_arch_smells, mod_arch_smells, rem_arch_smells, new_design_smells, mod_design_smells, rem_design_smells, new_impl_smells, mod_impl_smells, rem_impl_smells)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        compare_quantify(sys.argv[1])
    else:
        print('Usage instruction: compare_quantify <path>')