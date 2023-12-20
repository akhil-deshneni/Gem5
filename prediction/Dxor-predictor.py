from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
import os, m5
from m5.objects import *

# Create a system and configure it
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()
executable = None


def DXORBranchPredictor(num_entries, history_length):
    dxor_predictor = DXOR()
    return dxor_predictor


def DXOR():
    return {
        "cpu_pred": system.cpu.branchPred,
        "totalBranches": 1000,
        "architecure": "DXOR",
        "history_length": 15,
        "num_entries": 1024,
        "plot_path": "./task_output/dxor_performance_plot.png",
    }


# Create an X86-based CPU (AtomicSimpleCPU)
system.cpu = DerivO3CPU()

bp = LocalBP()
prediction = DXOR()
# Create a memory system
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.membus = SystemXBar()

# Create a system port
system.system_port = system.membus.cpu_side_ports

# Create a Gshare branch predictor
DXOR_predictor = DXORBranchPredictor(num_entries=1024, history_length=10)
system.cpu.branchPred = bp

os.system(f"python3 {executable}/dxor.py")
os.system(f"python3 {executable}/branch_predict_results.py")

# Create a simulation object
root = Root(full_system=True, system=system)

# Start the simulation
m5.instantiate()

# Run the simulation for a specified number of instructions
exit_event = m5.simulate(1000000)

bhr = (11, 17)
predictor_structure = 2
event_results = predictBranch(bhr, predictor_structure)

# Get branch prediction statistics
total_branches = DXOR_predictor.totalBranches
mispredicted_branches = DXOR_predictor.mispredictedBranches

print("Successfully run DXOR branch prediction algorithm")
