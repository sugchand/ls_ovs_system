import subprocess
import getpass
from enum import Enum, unique
import os

@unique
class SYS_OP(Enum):
    GET_KERNEL_VERSION          = 1
    GET_DPDK_VERSION            = 3
    GET_QEMU_VERSION            = 4
    GET_DISTRO_VERSION          = 5
    GET_DPDK_PORT_INFO          = 6
    GET_HUGEPAGE_INFO           = 7
    GET_INSTALL_DIR             = 8
    GET_OVS_LOGS                = 9
    GET_CPU_INFO                = 10

    LIST_DIR                    = 11

class linux_system:
    # The directory sets that must be set to collect all the information.
    CMD_SET_DICT = {
                    SYS_OP.GET_KERNEL_VERSION : "uname -a",
                    SYS_OP.GET_DPDK_VERSION : None,
                    SYS_OP.GET_HUGEPAGE_INFO : "cat /proc/meminfo |grep Huge",
                    SYS_OP.GET_DISTRO_VERSION : "lsb_release -a",
                    SYS_OP.LIST_DIR : "ls -la"
                    }
    FILE_NAME = "/tmp/ovs-logs.log"
    fp = None

    def __init__(self, ovs_install_dir, dpdk_install_dir, qemu_install_dir):
        self.fp = open(self.FILE_NAME, "w")
        self.OVS_INSTALL_DIR = ovs_install_dir
        self.DPDK_INSTALL_DIR = dpdk_install_dir
        self.qemu_INSTALL_DIR = qemu_install_dir

    def __del__(self):
        self.fp.close()

    def run_command(self, cmd, cmd_cwd = None, *args):
        exec_cmd = []
        if getpass.getuser() != "root":
            cmd = "sudo " + cmd
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
        (res, err) = self.run_command(cmd, cmd_dir)
        return (cmd, res, err)

    def get_ovs_run_sock_dir(self):
        log_file = None
        run_dir = None
        if os.path.isfile("/usr/local/var/log/openvswitch/ovs-vswitchd.log"):
            log_file = "/usr/local/var/log/openvswitch/ovs-vswitchd.log"
            run_dir = "/usr/local/var/run/openvswitch/"
        elif os.path.isfile("/var/log/openvswitch/ovs-vswitchd.log"):
            log_file = "/var/log/openvswitch/ovs-vswitchd.log"
            run_dir = "/var/run/openvswitch/"
        return(log_file, run_dir)

    def get_ovs_config_stats(self):
        exec_cmd_dir = None
        ovs_res = '\n'
        self.write_cmd_to_log(None, None, None, msg = "OVS config & stats :- ")
        if self.OVS_INSTALL_DIR != "":
            exec_cmd_dir = os.path.join(self.OVS_INSTALL_DIR, "utilities")
        (res, err) = self.run_command("./ovs-vsctl --version",
                                      cmd_cwd=exec_cmd_dir)
        ovs_res = ovs_res + "ovs-vsctl --version\n" + res + "\n\n"
        (res, err) = self.run_command("./ovs-vsctl show", cmd_cwd=exec_cmd_dir)
        ovs_res = ovs_res + "ovs-vsctl show\n" + res + "\n\n"
        (res, err) = self.run_command("./ovs-appctl dpctl/show -s",
                                      cmd_cwd=exec_cmd_dir)
        ovs_res = ovs_res + "ovs-appctl dpctl/show -s\n" + res + "\n\n"
        (res, err) = self.run_command(
                     "./ovs-appctl dpctl/dump-flows netdev@ovs-netdev",
                     cmd_cwd=exec_cmd_dir)
        ovs_res = ovs_res + "ovs-appctl dpctl/dump-flows" + res + "\n\n"
        (res, err) = self.run_command("./ovs-vsctl list-br",
                                      cmd_cwd=exec_cmd_dir)
        ovs_res = ovs_res + "ovs-vsctl list-br" + "\n" + res + "\n\n"
        if not err:
            br_list = filter(None, res.split('\n'))
        else:
           br_list = []
        for br in br_list:
            (res, err) = self.run_command("./ovs-ofctl show " + br,
                                          cmd_cwd=exec_cmd_dir)
            ovs_res = ovs_res + "ovs-ofctl show " + br + "\n" + res + "\n\n"
            (res, err) = self.run_command("./ovs-ofctl dump-flows " + br,
                                          cmd_cwd=exec_cmd_dir)
            ovs_res = ovs_res + "ovs-ofctl dump-flows " + br + "\n" + res + "\n\n"
        self.write_to_log(ovs_res)

    def write_to_log(self, str):
        self.fp.write(str)

    def write_cmd_to_log(self, exec_cmd, res, err, msg=""):
        if exec_cmd == None:
            exec_cmd = "None"
        if res == None:
            res = "None"
        if err == None:
            err = "None"
        self.fp.write("#######################################################\n")
        self.fp.write(msg)
        self.fp.write("\ncmd :- " + exec_cmd + "\n")
        self.fp.write("cmd err code :- " + err + "\n")
        self.fp.write(res)
        self.fp.write("\n#######################################################\n")

    def get_ovs_hw_info(self):
        # Collect cpu core mask of OVS and QEMU
        pass

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

    def write_cmd_to_log(self, exec_cmd, res, err):
        pass

    def get_ovs_run_dir(self):
        pass

    def get_ovs_config_stats(self):
        pass

    def get_ovs_hw_info(self):
        pass

def get_kernel_version(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_KERNEL_VERSION)
    sys_obj.write_cmd_to_log(cmd, res, err)

def get_ovs_version():
    pass

def get_dpdk_version():
    pass

def get_qemu_version():
    pass

def get_distro_version(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_DISTRO_VERSION)
    sys_obj.write_cmd_to_log(cmd, res, err)

def get_dpdk_port_info():
    pass

def get_hugepage_info(sys_obj):
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.GET_HUGEPAGE_INFO)
    sys_obj.write_cmd_to_log(cmd, res, err)

def get_install_dir():
    pass

def get_ovs_logs(sys_obj):
    (log_file, sock_dir) = sys_obj.get_ovs_run_sock_dir()
    if log_file == None or sock_dir == None:
        sys_obj.write_cmd_to_log("", "Cannot get ovs logs", "Files are missing")
        return
    with open(log_file) as log_fp:
        sys_obj.write_cmd_to_log(None, None, None, msg = "OVS logs :- ")
        for line in log_fp:
            sys_obj.write_to_log(line)
    (cmd, res, err) = sys_obj.get_sys_info(SYS_OP.LIST_DIR, cmd_dir = sock_dir)
    sys_obj.write_cmd_to_log(cmd, res, err, msg = "OVS socket directory:- ")
    sys_obj.get_ovs_config_stats()

def get_cpu_info(sys_obj):
    # get Host CPU and cores that used by OVS and qemu.
    pass

def main():
    OVS_INSTALL_DIR = ""
    DPDK_INSTALL_DIR = ""
    QEMU_INSTALL_DIR = ""
    sys_obj = None
    if os.name == 'posix':
        #Linux based system.
        OVS_INSTALL_DIR = None
        DPDK_INSTALL_DIR = None
        QEMU_INSTALL_DIR = None
        data = raw_input("Enter OVS source directory(Enter to skip):")
        if data:
            OVS_INSTALL_DIR = data.strip()
        data = raw_input("Enter DPDK source directory(Enter to skip):")
        if data:
            DPDK_INSTALL_DIR = data.strip()
        data = raw_input("Enter QEMU source dir(Enter to skip)")
        if data:
            DPDK_INSTALL_DIR = data.strip()
        sys_obj = linux_system(OVS_INSTALL_DIR, DPDK_INSTALL_DIR,
                               QEMU_INSTALL_DIR)
        get_distro_version(sys_obj)
        get_kernel_version(sys_obj)
        get_hugepage_info(sys_obj)
        get_ovs_logs(sys_obj)
    else:
        print("The tool doesnt support this OS, Exiting...")
        return

main()
