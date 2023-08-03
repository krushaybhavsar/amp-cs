def split_eggs(basket: list[int]) -> tuple[list[int], list[int], list[int]]:
    """Splits a basket of eggs into 3 groups of equal size.
    Assumes that the number of eggs in the basket is a power of 3.

     Args:
      basket (list[int]): A list of integer weights for each egg in the basket

     Returns:
      list1: a list of first third of egg weights in the basket
      list2: a list of middle third of egg weights in the basket
      list3: a list of last third of egg weights in the basket

     Example
     -------
     >>>split_eggs([10, 10, 10, 11, 10, 10, 10, 10, 10])
     [10,10,10], [11, 10, 10], [10, 10, 10]
    """
    length = len(basket)

    group1 = basket[0 : length // 3]
    group2 = basket[length // 3 : length // 3 * 2]
    group3 = basket[length // 3 * 2 : length]

    return group1, group2, group3


def compare_egg_groups(left_group: list[int], right_group: list[int]) -> str:
    """Compares the weight of 2 groups like a balance.
    Calling the compare function counts as 1 weighing.

    Args:
     left_group (list[int]): A list of integer weights for the eggs on the left side of the balance
     right_group  (list[int]): A list of integer weights for the eggs on the right side of the balance

    Returns:
     "left", "right", or "equal" depending on which group is heavier

    Example
    -------
    >>>compare_egg_groups([10,10,10], [11, 10, 10])
    "right"
    """
    if sum(left_group) > sum(right_group):
        return "left"
    elif sum(right_group) > sum(left_group):
        return "right"
    else:
        return "equal"


def find_fake_group(
    left_group: list[int], right_group: list[int], extra_group: list[int]
) -> tuple[list[int], str]:
    """Finds the fake egg group, knowing that the fake egg is heavier

    Args:
     left_group (list[int]): A list of integer weights for the eggs on the left side of the balance
     right_group  (list[int]): A list of integer weights for the eggs on the right side of the balance
     extra_group  (list[int]): A list of integer weights for the eggs that aren't being weighed

    Returns:
      the group with the fake egg (list[int])
     "left", "right", or "equal" depending on which side of the scale is heavier

    Example
    -------
    >>>find_fake_group([10,10,10], [11, 10, 10], [10, 10, 10])
    [11, 10, 10]
    "right"
    """
    result = compare_egg_groups(left_group, right_group)

    if result == "left":
        return left_group, "left"
    elif result == "right":
        return right_group, "right"
    else:
        return extra_group, "equal"


def find_heavier_egg_nonrecursive(basket: list[int]) -> tuple[int, int]:
    """
    Uses a while loop to repeatedly divide the pile into 3 smaller groups of eggs.
    - Number of eggs in the basket will be equal to a power of 3.
    - Makes use of provided splitEggs(basket) function to divide eggs into three groups
      -To arrive at the same number of weighings as the autograder, use the given definition of the split_eggs function.

        Args:
        basket (list[int]): A list of egg weights

        Returns:
        the location of the fake egg, along with the number of weighings used to find the egg
            - If there is no fake Egg, return -1 for index
            - If the function is called on an empty basket of eggs, return -1, 0

        Examples
        --------
        >>>find_heavier_egg_nonrecursive([10, 10, 10, 10, 10, 10, 10, 10, 10])
        -1, 3

        >>>find_heavier_egg_nonrecursive([10, 10, 10, 10, 10, 11, 10, 10, 10])
        5, 3
    """
    if len(basket) == 0:
        return -1, 0

    curr_group = basket[:]  # Make a copy of basket to preserve the original list
    # This will help us find the location of the fake egg at the end
    weight_counter = 0

    while len(curr_group) > 1:  # Once you're down to one egg you've found the fake
        group1, group2, group3 = split_eggs(curr_group)
        curr_group, result = find_fake_group(group1, group2, group3)
        weight_counter += 1

    egg_types = set()
    for egg in basket:
        egg_types.add(egg)
    if len(egg_types) == 1:
        return -1, weight_counter

    fake = curr_group[0]  # The fake is the only egg in the list
    return basket.index(fake), weight_counter


def has_fake(basket: list[int]) -> bool:
    egg_types = set()
    for egg in basket:
        egg_types.add(egg)

    return len(egg_types) != 1 and len(egg_types) != 0


def find_heavier_egg_recursive(
    basket: list[int], num_weighings=0, orgList=[]
) -> tuple[int, int]:
    """Uses recursion to repeatedly divide the pile into 3 smaller groups of eggs.
    Assumes:
       - Number of eggs in the basket will be equal to a power of 3.
       - There will be exactly 1 or 0 heavier eggs
       - Makes use of provided splitEggs(basket) function to divide eggs into three groups
         -To arrive at the same number of weighings as the autograder, use the given definition of the split_eggs function.

     Args:
       basket (list): A list of egg weights with length equal to a power of 3
       numWeighings (int): The current number of egg weighings
       orgList: (list): The original egglist (used to find the position of the fake egg)

     Returns:
       int: The index of the fake egg in the original list
       int: The number of weighings used to find the egg

     Examples
     --------
     >>>find_heavier_egg_recursive([10, 10, 10, 10, 10, 10, 10, 10, 10])
     -1, 3

     >>>find_heavier_egg_recursive([10, 10, 10, 10, 10, 11, 10, 10, 10])
     5, 3
    """
    if len(basket) == 0:
        return -1, 0

    if num_weighings == 0:
        if not has_fake(basket):
            return -1, 0

    if len(orgList) == 0:
        orgList = basket[:]

    if len(basket) == 1:
        return orgList.index(basket[0]), num_weighings

    group1, group2, group3 = split_eggs(basket)
    result = compare_egg_groups(group1, group2)

    if result == "left":
        return find_heavier_egg_recursive(group1, num_weighings + 1, orgList)
    elif result == "right":
        return find_heavier_egg_recursive(group2, num_weighings + 1, orgList)
    else:
        return find_heavier_egg_recursive(group3, num_weighings + 1, orgList)


def find_lighter_or_heavier_egg(basket: list[int]) -> tuple[str, int]:
    """Determines which egg (if any) is a fake, as well as the type of fake

    Assumes:
       - Number of eggs in the basket will be equal to a power of 3.
       - There will be exactly 1 or 0 heavier or lighter eggs
       - Makes use of provided splitEggs(basket) function to divide eggs into three groups

     Args:
       basket (list): A list of egg weights with length equal to a power of 3

     Returns:
       str: a label indicating which type of fake egg has been found: 'heavier', 'lighter', or 'no fake'
       int: The index of the fake egg in the original list

     Examples
     --------
     >>>find_lighter_or_heavier_egg([10, 10, 10, 10, 10, 10, 10, 10, 10])
     'no fake', -1

     >>>find_lighter_or_heavier_egg([10, 10, 10, 10, 10, 9, 10, 10, 10])
     'lighter', 5
    """

    if len(basket) == 0:
        return "no fake", -1

    if len(basket) == 1:
        return "no fake", 0

    egg_weight_distribution = {}

    for egg in basket:
        if egg in egg_weight_distribution:
            egg_weight_distribution[egg] += 1
        else:
            egg_weight_distribution[egg] = 1

    if len(egg_weight_distribution) == 1:
        return "no fake", -1

    fake = 0
    if len(egg_weight_distribution) == 2:
        for egg in egg_weight_distribution:
            if egg_weight_distribution[egg] == 1:
                fake = egg
                break

        if fake == max(egg_weight_distribution):
            return "heavier", basket.index(fake)
        else:
            return "lighter", basket.index(fake)


if __name__ == "__main__":
    basket1 = [10, 10, 10, 9, 10, 10, 10, 10, 10]
    basket2 = [10, 10, 10, 10, 10, 11, 10, 10, 10]

    basket3 = [
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        11,
        10,
        10,
        10,
        10,
    ]
    basket4 = [10, 10, 10, 10, 10, 10, 10, 10, 10]

    print(find_heavier_egg_recursive([10, 10, 10, 10, 10, 10, 10, 10, 10]))
