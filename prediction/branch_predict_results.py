import matplotlib.pyplot as plt
from dxor import predictBranch as dxor_predictBranch
from gshare import predictBranch as gshare_predictBranch
from lp import predictBranch as lp_predictBranch
import os


def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
    # print('Successfully emptied the directory: ', directory)


empty_directory("./task_output")


def plot_results():

    # Call the function to empty the directory
    empty_directory("./task_output")

    # Plot Data
    cache_sizes = [4, 8, 16, 32, 64, 128, 256]  # in KB
    performance_bars = [
        95.0,
        95.5,
        96.0,
        96.5,
        97.0,
        97.5,
        98.0,
        98.5,
        99.0,
        99.5,
        100.0,
    ]

    # Data Fetch
    dxor_result = (dxor_predictBranch((11, 17), 2, False)).get("dxor_result")
    gshare_result = (gshare_predictBranch((11, 17), 2, False)).get(
        "gshare_result"
    )
    lp_result = (lp_predictBranch((11, 17), 2, False)).get("lp_result")

    # Plotting
    # Create a scatter plot
    plt.plot(cache_sizes, dxor_result, marker="o", color="green", label="dxor")
    plt.plot(
        cache_sizes, gshare_result, marker="^", color="blue", label="gshare"
    )
    plt.plot(cache_sizes, lp_result, marker="s", color="red", label="lp")

    # Set the axis labels
    plt.xlabel("Cache Size (KB)")
    plt.ylabel("Performance (%)")

    # Set the axis limits
    plt.xlim(4, 256)
    plt.ylim(95.0, 100.0)

    # Set x-axis ticks
    plt.xscale("log", base=2)
    plt.xticks(cache_sizes, labels=[str(size) + "kB" for size in cache_sizes])
    plt.yticks(performance_bars)

    # Add legend
    plt.legend()
    plt.title("Cache Size vs Performance")
    plt.grid(True)

    # plt.savefig('./task_output/dxor_performance_plot.png')

    # Call the function to empty the directory
    empty_directory("./task_output")

    # Save the plot
    plt.savefig("./task_output/performance_plot.png")

    print("Successfully plotted the branch prediction results \n")
    print("Results are saved in /task_output/combined_performance_plot.png \n")


if __name__ == "__main__":
    plot_results()
