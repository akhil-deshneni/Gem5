import m5
from m5.objects import *

# Create a system and configure it
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Create an X86-based CPU (AtomicSimpleCPU)
system.cpu = AtomicSimpleCPU()
# system.cpu.isa = X86_ISA()  # Set the ISA to X86

# Create a memory system
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.membus = SystemXBar()

# Create a system port
system.system_port = system.membus.cpu_side_ports

# Create a local branch predictor
local_predictor = LocalBP()
system.cpu.branchPred = local_predictor

# Create a process and set the command to execute
process = Process()
process.cmd = [""]  # Replace with the actual command to run

# Set the workload
workload = SEWorkload()
workload.processes = [process]

# Create a simulation object
root = Root(full_system=True, system=system)

# Start the simulation
m5.instantiate(workload)

# Run the simulation for a specified number of instructions
exit_event = m5.simulate(1000000, workload=workload)

# Get branch prediction statistics
total_branches = local_predictor.predictor.totalBranches
mispredicted_branches = local_predictor.predictor.mispredictedBranches

print("Total Branches:", total_branches)
print("Mispredicted Branches:", mispredicted_branches)

print("Successfully run local branch prediction algorithm")
