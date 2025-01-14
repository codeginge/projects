import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_menger_sponge(level, size, offset=(0, 0, 0)):
    if level == 0:
        return [offset + (size,)]
    
    sub_sponges = []
    sub_size = size // 3
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i != 1 or j != 1 or k != 1:
                    new_offset = (offset[0] + i * sub_size, offset[1] + j 
* sub_size, offset[2] + k * sub_size)
                    sub_sponges.extend(generate_menger_sponge(level - 1, 
sub_size, new_offset))
    
    return sub_sponges

def plot_menger_sponge(level, size):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    sponges = generate_menger_sponge(level, size)
    for sponge in sponges:
        ax.add_collection3d(Poly3DCollection([list(zip(*sponge))], 
alpha=1, facecolor='gray', edgecolor='black'))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Menger Sponge')
    ax.set_xlim([0, size])
    ax.set_ylim([0, size])
    ax.set_zlim([0, size])
    
    plt.show()

# Example usage
plot_menger_sponge(level=2, size=100)

