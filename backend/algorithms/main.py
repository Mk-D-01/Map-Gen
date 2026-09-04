import random

def generate_prototype_grid(seed,width=20,height=20):
    random.seed(seed)

    grid = [
        [1 if random.random() <0.45 else 0 for _ in range(width)]
        for _ in range(height)
    ]

    def wall_neighbours(x,y):
       count=0
       for dy in (-1,0,1):
           for dx in (-1,0,1):
               if dx ==0 and dy==0:
                   continue
               nx,ny= x+dx, y+dy

               if nx<0 or nx>=width or ny<0 or ny>=height:
                   count+=1
               elif grid[ny][nx]==1:
                   count+=1
       return count 

    smoothed =[row[:] for row in grid]
    for y in range(height):
        for x in range(width):
            smoothed[y][x] = 1 if wall_neighbours(x,y) >4 else 0

    return smoothed


if __name__ == "__main__":
    g1= generate_prototype_grid(42)
    g2= generate_prototype_grid(42)
    assert g1==g2, "Determinism check FAILED - grids differ!"
    print("Determinism check passed: same seed produces identitcal grids.")

    sample = generate_prototype_grid(42, width=15, height=10)
    for row in sample:
        print("".join("#" if cell == 1 else "." for cell in row))