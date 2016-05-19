import subprocess
import getpass
from enum import Enum, unique
import os

@unique
class SYS_OP(Enum):
    GET_KERNEL_VERSION          = 1
    GET_OVS_VERSION             = 2
    GET_DPDK_VERSION            = 3
    GET_QEMU_VERSION            = 4
    GET_LINUX_DISTRO            = 5
    GET_DPDK_PORT_INFO          = 6
    GET_HUGEPAGE_INFO           = 7
    GET_INSTALL_DIR             = 8
    GET_OVS_LOGS                = 9
    GET_CPU_INFO                = 10
    GET_OVS_DIR                 = 11
    GET_DPDK_DIR                = 12
    GET_QEMU_DIR                = 13

class linux_system:
    # The directory sets that must be set to collect all the information.
    CMD_SET_DICT = { 
                    SYS_OP.GET_KERNEL_VERSION : "uname -a",
                    SYS_OP.GET_OVS_VERSION : "ovs-vswitchd --version",
                    SYS_OP.GET_DPDK_VERSION : None,
                    SYS_OP.GET_HUGEPAGE_INFO : "cat /proc/meminfo |grep Huge",
                    SYS_OP.GET_LINUX_DISTRO : "lsb_release -a"
                    }
    FILE_NAME = "/tmp/ovs-logs.log"
    fp = None

    def __init__(self):
        self.fp = open(self.FILE_NAME, "w")

    def __del__(self):
        self.fp.close()

    def run_command(self, cmd, cmd_cwd = None, *args):
        exec_cmd = []
        exec_cmd.append(cmd)

        if(len(args)):
            exec_cmd = exec_cmd + list(args)

        exec_cmd = filter(None, exec_cmd)
        print exec_cmd

        try:
            out = subprocess.Popen(exec_cmd, cwd=cmd_cwd, shell=True,
                                            stdout=subprocess.PIPE)
        except Exception as e:
            print("Failed to run the bash command, " + e)
        res, err = out.communicate()
        return(res, err)

    def run_command_with_list_args(self, cmd_cwd, cmd, args):
        self.run_command(cmd, *args)

    def get_sys_info(self, cmd_opt, cmd_dir = None):
        cmd = self.CMD_SET_DICT[cmd_opt]
        if getpass.getuser() != "root":
            cmd = "sudo " + cmd
        (res, err) = self.run_command(cmd, cmd_dir)
        return (cmd, res, err)

    def write_to_log(self, exec_cmd, res, err):
        if exec_cmd == None:
            exec_cmd = "None"
        if res == None:
            res = "None"
        if err == None:
            err = "None"
        self.fp.write("#######################################################\n")
        self.fp.write("cmd :- " + exec_cmd + "\n")
        self.fp.write("cmd err code :- " + err + "\n")
        self.fp.write(res)
        self.fp.write("\n#######################################################\n")

class windows_system:
    FILE_NAME = "C:/temp/ovs-logs.log"
    fp = None

    def __init__(self):
        self.fp = open(self.FILE_NAME, "w")

    def run_command(self, cmd, cmd_cwd = None, *args):
        pass

    def run_command_with_list_args(self, cmd_cwd, cmd, args):
        pass

    def get_sys_info(self, cmd_opt,cmd_dir = None):
        pass

    def write_to_log(self, exec_cmd, res, err):
        pass

def get_kernel_version(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_KERNEL_VERSION)
    sys_obj.write_to_log(cmd, res, err)

def get_ovs_version():
    pass

def get_dpdk_version():
    pass

def get_qemu_version():
    pass

def get_linux_distro(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_LINUX_DISTRO)
    sys_obj.write_to_log(cmd, res, err)

def get_dpdk_port_info():
    pass

def get_hugepage_info(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_HUGEPAGE_INFO)
    sys_obj.write_to_log(cmd, res, err)

def get_install_dir():
    pass

def get_ovs_logs():
    pass

def get_cpu_info():
    # get Host CPU and cores that used by OVS and qemu.
    pass

def main():
    OVS_INSTALL_DIR = None
    DPDK_INSTALL_DIR = None
    QEMU_INSTALL_DIR = None
    sys_obj = None
    if os.name == 'posix':
        #Linux based system.
        OVS_INSTALL_DIR = "/usr/src/openvswitch"
        DPDK_INSTALL_DIR = "/usr/src/dpdk"
        QEMU_INSTALL_DIR = "usr/src/qemu"
        data = raw_input("Enter OVS install dir(" + OVS_INSTALL_DIR + "):")
        if data:
            OVS_INSTALL_DIR = data.strip()
        data = raw_input("Enter DPDK install dir(" + DPDK_INSTALL_DIR + "):")
        if data:
            DPDK_INSTALL_DIR = data.strip()
        data = raw_input("Enter QEMU install dir(" + QEMU_INSTALL_DIR + "):")
        if data:
            DPDK_INSTALL_DIR = data.strip()    
        sys_obj = linux_system()
        get_linux_distro(sys_obj)
        get_kernel_version(sys_obj)
        get_hugepage_info(sys_obj)
        
    else:
        print("The tool doesnt support this OS, Exiting...")
        return

main()