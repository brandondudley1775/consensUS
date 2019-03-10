import matplotlib.pyplot as plt
import sys

color_list = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
# assume labels are comma-separated first arg, sys.argv[1]
labels = sys.argv[1].split(",")

# assume sizes are comma-separated second arg, sys.argv[2]
sizes = sys.argv[2].split(",")

# filename is last argument
filename = sys.argv[3]

#labels = ['Cookies', 'Jellybean', 'Milkshake', 'Cheesecake']
#sizes = [38.4, 40.6, 20.7, 10.3]
plt.title(sys.argv[4])
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.savefig(filename)