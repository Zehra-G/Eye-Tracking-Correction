
import numpy as np

def H_logis(x, D_high, D_low):
    b = -(D_high + D_low) * np.log(9) / (D_high - D_low)
    s = -2 * np.log(9) / (D_high - D_low)
    return 1 / (1 + np.exp(-b + x * s))

def G_cor(G, N, c=0.4, p=0.00125):
    return G * (c + N * p)

def fitness_function(ox, oy, fixations, AOIs, D_high, D_low):
    N = len(fixations)
    G_sum = 0
    
    for fx, fy in fixations:
        min_distance = float('inf')
        
        for aoi in AOIs:
            distance = np.sqrt((fx + ox - aoi[0]) ** 2 + (fy + oy - aoi[1]) ** 2)
            min_distance = min(min_distance, distance)
        
        G_raw = H_logis(min_distance, D_high, D_low)
        G_sum += G_cor(G_raw, N)
    
    return G_sum / N

def find_optimal_offset(fixations, AOIs, offset_range=(-100, 100), step=1, D_high=10, D_low=20):
    best_offset = None
    best_fitness = -float('inf')
    
    for ox in range(offset_range[0], offset_range[1] + 1, step):
        for oy in range(offset_range[0], offset_range[1] + 1, step):
            fitness = fitness_function(ox, oy, fixations, AOIs, D_high, D_low)
            
            if fitness > best_fitness:
                best_fitness = fitness
                best_offset = (ox, oy)
    
    return best_offset, best_fitness

# Example usage
fixations = [(100, 100), (120, 130), (140, 120), (110, 90)]
AOIs = [(110, 110), (130, 130), (150, 120), (120, 100)]

best_offset, best_fitness = find_optimal_offset(fixations, AOIs)
print(f"Best offset: {best_offset}")
print(f"Best fitness: {best_fitness}")
