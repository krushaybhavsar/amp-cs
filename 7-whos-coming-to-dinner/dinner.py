def find_dislikes(friends: dict) -> set[tuple]:
    """Given a dictionary-based adjacency list of String-based nodes,
    returns a set of all edges in the graph (ie. dislikes who can't be invited together).

    Args:
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A set of edges in the graph represented as tuples
         - An edge should only appear once in the list.
         - Each edge should list node connections in alphabetical order.

    Example
    -------
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Eve':['Bob']
    }
    >>>find_dislikes(friends)
    {('Alice','Bob'),('Bob','Eve')}

    """
    dislikes = set()

    for friend in friends:
        for enemy in friends[friend]:
            if (friend, enemy) not in dislikes and (enemy, friend) not in dislikes:
                sorted_pair = sorted([friend, enemy])
                dislikes.add((sorted_pair[0], sorted_pair[1]))

    return dislikes


def generate_all_subsets(friends: dict) -> list[list[str]]:
    """Converts each number from 0 to 2^n - 1 into binary and uses the binary representation
    to determine the combination of guests and returns all possible combinations

    Args:
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A list of all possible subsets of friends to invite, represented as lists of strings

    Example
    -------
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Eve':['Bob']
    }
    >>>generate_all_subsets(friends)
    [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
    """
    friend_list = list(friends.keys())
    n = len(friends)

    all_subsets = []

    for i in range(2**n):
        num = i  # convert each number in the range to a binary string
        new_subset = []
        for j in range(n):  # to_binary_division approach
            if num % 2 == 1:  # 1 indicates the guest is included
                new_subset = [friend_list[n - 1 - j]] + new_subset
            num = num // 2
        all_subsets.append(new_subset)

    return all_subsets


def filter_bad_invites(all_subsets: list, friends: dict) -> list[list[str]]:
    """Removes subsets from all_subsets that contain any pair of friends who
    are in a dislike relationship

    Args:
        all_subsets: a list of all possible friend combinations, each reresented as a list of strings
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A list containing only friend combinations that exclude dislike pairs

    Example
    -------
    >>>all_subsets = [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice'],
        'Eve':[]
    }
    >>>filter_bad_invites(all_subsets, friends)
    [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve']]
    """

    good_invites = []
    for subset in all_subsets:
        bad_subset = False
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                if subset[j] in friends[subset[i]] or subset[i] in friends[subset[j]]:
                    bad_subset = True
        if not bad_subset:
            good_invites.append(subset)

    return good_invites


def filter_no_dislikes(friends: dict) -> tuple[list, dict]:
    """An optimization that removes friends who are not in any dislikes relationships,
    prior to generating combinations and add them to the invite list.

    Args:
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A tuple containing:
         - list of friends not in dislike relations AND
        - resulting dictionary with these friends removed

    Example
    -------
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    >>>filter_no_dislikes(friends)
    (['Cleo', 'Don'],
    {
        'Alice': ['Bob'],
        'Bob': ['Alice', 'Eve'],
        'Eve': ['Bob']
    })
    """

    no_dislikes = []
    problem_friends = {}

    for friend in friends:
        good_person = True
        for f in friends:
            if friend in friends[f]:
                good_person = False
        if len(friends[friend]) == 0 and good_person:
            no_dislikes.append(friend)

    for friend in friends:
        if friend not in no_dislikes:
            problem_friends[friend] = friends[friend]

    return no_dislikes, problem_friends


# friends = {
#     "Alice": [],
#     "Bob": [],
#     "Cleo": [],
#     "Don": [],
#     "Eve": ["Bob"],
# }
# print(filter_no_dislikes(friends))
# (["Cleo", "Don"], {"Alice": ["Bob"], "Bob": ["Alice", "Eve"], "Eve": ["Bob"]})


def invite_to_dinner(friends: dict) -> list[str]:
    """Finds the invite combo with the maximum number of guests

    Args:
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A list of friends to invite to dinner which maximizes the number of friends on the list

    Example
    -------
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    >>>invite_to_dinner(friends)
    ['Alice', 'Eve', 'Cleo', 'Don']
    """
    definite_invites, problem_friends = filter_no_dislikes(friends)
    all_subsets = generate_all_subsets(problem_friends)
    good_subsets = filter_bad_invites(all_subsets, problem_friends)

    # find the subset which maximizes number of invites
    invite_list = []
    for i in good_subsets:
        if len(i) > len(invite_list):
            invite_list = i

    # recombine with definite invites
    invite_list += definite_invites

    return invite_list


def invite_to_dinner_optimized(friends: dict) -> list:
    """Finds the combination with the maximum number of guests without storing all combinations

    Functions the same as invite_to_dinner without storing all subsets
    i.e. invite_to_dinner stores the variable all_subsets

    Args:
        friends: dictionary-based adjacency matrix representing friend relations

    Returns:
        A list of friends to invite to dinner which maximizes the number of friends on the list

    Example
    -------
    >>>friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    >>>invite_to_dinner(friends)
    ['Alice', 'Eve', 'Cleo', 'Don']
    """

    invite_list = []
    definite_invites, problem_friends = filter_no_dislikes(friends)
    all_subsets = generate_all_subsets(problem_friends)

    for subset in all_subsets:
        if len(subset) > len(invite_list):
            bad_subset = False
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    if (
                        subset[j] in friends[subset[i]]
                        or subset[i] in friends[subset[j]]
                    ):
                        bad_subset = True
            if not bad_subset:
                invite_list = subset

    invite_list += definite_invites

    return invite_list


# if __name__ == "__main__":
#     friends = {
#         "Alice": ["Bob"],
#         "Bob": ["Alice", "Eve"],
#         "Cleo": [],
#         "Don": [],
#         "Eve": ["Bob"],
#     }
#     print(invite_to_dinner(friends))
#     print(invite_to_dinner_optimized(friends))

#     friends_2 = {"Alice": ["Bob"], "Bob": ["Alice", "Eve"], "Eve": ["Bob"]}
#     print(invite_to_dinner(friends_2))
#     print(invite_to_dinner_optimized(friends_2))

#     friends_3 = {
#         "Asa": [],
#         "Bear": ["Cate"],
#         "Cate": ["Bear", "Dave"],
#         "Dave": ["Cate", "Eve"],
#         "Eve": ["Dave"],
#         "Finn": ["Ginny", "Haruki", "Ivan"],
#         "Ginny": ["Finn", "Haruki"],
#         "Haruki": ["Ginny"],
#         "Ivan": ["Finn"],
#     }
#     print(invite_to_dinner(friends_3))
#     print(invite_to_dinner_optimized(friends_3))
