import random


class Field:
    def __init__(self, size, mirrors, rotators):
        # Initialize the field with given size and obstacles.
        self.size = size
        self.mirrors = mirrors
        self.rotators = rotators
        # Generate the field layout with mirrors, rotators, and river.
        self.field = self.generate()

    def generate(self):
        # Ensure the field size is at least 4x4.
        if self.size < 4:
            raise ValueError("Field size must be at least 4")

        # Check that the number of mirrors and rotators doesn't exceed the total field cells.
        if self.mirrors + self.rotators > self.size * self.size:
            raise ValueError("Too many mirrors and rotators for the field size")

        # Initialize the field structure with mirrors, rotators, and 'S' (safe) for all cells.
        field = {
            "mirrors": [],
            "rotators": [],
            "source": (),
            "mouth": (),
            "crocodile": (),
            "walls": (), # (x1, y1), (x2, y2) |x1 - x2| = 1 or |y1 - y2| = 1
            "field": [["S" for _ in range(self.size)] for _ in range(self.size)]
        }

        # Randomly place mirrors on the field.
        for mirror in range(self.mirrors):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            t = random.choice(["V", "H", "VH"])

            field["mirrors"].append((x, y, t))


        # Randomly place rotators, ensuring they don't overlap with mirrors.
        for rotator in range(self.rotators):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while (x, y) in field["mirrors"]:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            t = random.choice(["CW", "CCW"])

            field["rotators"].append((x, y, t))

        # Define the initial position for the river.
        pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        field["source"] = pos
        # Determine the river length, ensuring it's within reasonable limits.
        length = random.randint(int(self.size ** 2 / 3), int(self.size ** 2 * 2 / 3))
        placed = 0
        # Define possible directions for river expansion: right, down, left, up.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        d = "M"

        crocodile = (pos[0], pos[1])
        direction = random.choice(directions)
        while not (0 <= crocodile[0] + direction[0] < self.size and 0 <= crocodile[1] + direction[1] < self.size):
            direction = random.choice(directions)

        crocodile = (crocodile[0] + direction[0], crocodile[1] + direction[1])
        field["field"][crocodile[0]][crocodile[1]] = "C"

        # Place river segments until the desired length is reached.
        while placed < length:
            x, y = pos
            # If the current cell is safe, convert it to river ('R').
            if field["field"][x][y] == "S":
                field["field"][x][y] = "R" + d
                field["mouth"] = (x, y)
                placed += 1

            # Choose a random direction to expand the river.
            d = random.randint(0, 3)
            direction = directions[d]
            d = "LURD"[d]

            max_iter = 50
            # Ensure the next cell is within bounds and safe before placing the river.
            while not (0 <= x + direction[0] < self.size and 0 <= y + direction[1] < self.size and
                       field["field"][x + direction[0]][y + direction[1]] == "S") and max_iter > 0:
                d = random.randint(0, 3)
                direction = directions[d]
                d = "LURD"[d]
                max_iter -= 1

            if max_iter == 0:
                break

            # Update the current position to the new cell.
            pos = (x + direction[0], y + direction[1])

        # Ensure the "A" point is placed on a safe cell.
        while field["field"][pos[0]][pos[1]] != "S":
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        # Mark the starting point with 'A'.
        field["field"][pos[0]][pos[1]] = "A"

        # Ensure the "H" point is placed on a safe cell.
        while field["field"][pos[0]][pos[1]] != "S":
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        # Mark the ending point with 'H'.
        field["field"][pos[0]][pos[1]] = "H"

        # Ensure the "T" point is placed on a safe cell.
        while field["field"][pos[0]][pos[1]] != "S":
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        # Mark the ending point with 'T'.
        field["field"][pos[0]][pos[1]] = "T"

        field["source"], field["mouth"] = field["mouth"], field["source"]
        field["field"][field["source"][0]][field["source"][1]] += "S"

        return field



if __name__ == '__main__':
    # Test the field generation with a 5x5 field, 3 mirrors, and 2 rotators.
    field = Field(5, 3, 2)
    print(field.field["mirrors"])
    print(field.field["rotators"])
    print(field.field["source"])
    print(field.field["mouth"])
    for row in field.field["field"]:
        for cell in row:
            print('{:>4}'.format(cell), end="")
        print()