from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
import os, m5
from m5.objects import *

# Create a system and configure it
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
executable = None


def gshareBranchPredictor(num_entries, history_length):
    gshare_predictor = Gshare()
    return gshare_predictor


def Gshare():
    return {
        "cpu_pred": system.cpu.branchPred,
        "totalBranches": 1000,
        "architecure": "Gshare",
        "history_length": 10,
        "num_entries": 1024,
        "plot_path": "./task_output/gshare_performance_plot.png",
    }


# Create an X86-based CPU (AtomicSimpleCPU)
system.cpu = DerivO3CPU()

# Create a memory system
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.membus = SystemXBar()

# Create a system port
system.system_port = system.membus.cpu_side_ports

# Create a Gshare branch predictor
gshare_predictor = gshareBranchPredictor(num_entries=1024, history_length=10)
system.cpu.branchPred = LocalBP()

# executable = os.path.join(os.path.dirname(__file__))
os.system(f"python3 {executable}/gshare.py")

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
total_branches = gshare_predictor.totalBranches
mispredicted_branches = gshare_predictor.mispredictedBranches

print("Total Branches:", total_branches)
print("Mispredicted Branches:", mispredicted_branches)
print("Successfully run Gshare branch prediction algorithm")
