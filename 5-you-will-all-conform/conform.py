def please_flip_original(caps: list[str]) -> list[str]:
    """
    Generates a minimal list of shouts needed to have all fan caps face the same direction.

    Args:
      caps: list of strings which are either 'F' (Forward) or 'B' (Backward)

    Return:
      a list of shouts, which could be empty if the list of caps is either empty or all the same direction
    """
    intervals = []
    interval_start = 0
    forward_count = backward_count = 0
    shouts = []

    if len(caps) == 0:
        return shouts

    # Step 1: Determine intervals where hats face the same direction
    for i in range(1, len(caps)):
        if caps[interval_start] != caps[i]:
            intervals.append(
                (interval_start, i - 1, caps[interval_start])
            )  # (start, end, direction)

            if caps[interval_start] == "F":
                forward_count += 1
            else:
                backward_count += 1
            interval_start = i  # new hat direction->new interval start

    intervals.append((interval_start, len(caps) - 1, caps[interval_start]))
    if caps[interval_start] == "F":
        forward_count += 1
    else:
        backward_count += 1

    # Step 2: Decide which way to flip based on hat direction with least number of intervals
    if forward_count < backward_count:
        flip_direction = "F"
    else:
        flip_direction = "B"

    # Step 3: Flip all of the intervals that match with the flip direction
    for t in intervals:
        if t[2] == flip_direction:
            if t[0] == t[1]:
                shouts.append(f"Person in position {str(t[0])} flip your cap!")
            else:
                shouts.append(
                    f"People in positions {str(t[0])} through {str(t[1])} flip your caps!"
                )
    return shouts


def please_flip_streamlined(caps: list[str]) -> list[str]:
    """
    Generates a minimal list of shouts needed to have all fan caps face the same direction.

      Args:
      caps: list of strings which are either 'F' (Forward) or 'B' (Backward)

      Return:
      a list of shouts, which could be empty if the list of caps is either empty or all the same direction
    """

    intervals = []
    interval_start = 0
    shouts = []

    if len(caps) == 0:
        return shouts

    for i in range(1, len(caps) + 1):
        if (i == len(caps)) or (caps[interval_start] != caps[i]):
            intervals.append((interval_start, i - 1, caps[interval_start]))
            interval_start = i

    if len(intervals) % 2 == 0:
        flip_direction = "B"
    else:
        if intervals[0][2] == "F":
            flip_direction = "B"
        else:
            flip_direction = "F"

    for t in intervals:
        if t[2] == flip_direction:
            if t[0] == t[1]:
                shouts.append(f"Person in position {str(t[0])} flip your cap!")
            else:
                shouts.append(
                    f"People in positions {str(t[0])} through {str(t[1])} flip your caps!"
                )
    return shouts


def please_flip_bare(caps: list[str]) -> list[str]:
    """
    Generates a minimal list of shouts needed to have all fan caps face the same direction, skipping
    fans with no cap.

      Args:
      caps: list of strings which are either 'F' (Forward) or 'B' (Backward) or 'H' (Bareheaded)

      Return:
      a list of shouts, which could be empty if the list of caps is either empty or all the same direction
    """
    intervals = []
    interval_start = 0
    shouts = []
    direction_tracker = 0

    if len(caps) == 0:
        return shouts

    for i in range(1, len(caps) + 1):
        if (i == len(caps)) or (caps[interval_start] != caps[i]):
            if caps[interval_start] == "F":
                direction_tracker += 1
            elif caps[interval_start] == "B":
                direction_tracker -= 1
            intervals.append((interval_start, i - 1, caps[interval_start]))
            interval_start = i

    if direction_tracker < 0:
        flip_direction = "F"
    else:
        flip_direction = "B"

    print(intervals)

    for t in intervals:
        if t[2] == flip_direction:
            if t[0] == t[1]:
                shouts.append(f"Person in position {str(t[0])} flip your cap!")
            else:
                shouts.append(
                    f"People in positions {str(t[0])} through {str(t[1])} flip your caps!"
                )

    return shouts


def please_flip_one_pass(caps: list) -> list:
    """
    Generates a minimal list of shouts needed to have all fan caps face the same direction using exactly 1 for loop

      Args:
      caps: list of strings which are either 'F' (Forward) or 'B' (Backward)

      Return:
      a list of shouts, which could be empty if the list of caps is either empty or all the same direction
    """
    interval_start = 0
    shouts = {"F": [], "B": []}

    if len(caps) == 0:
        return []

    for i in range(1, len(caps) + 1):
        if (i == len(caps)) or (caps[interval_start] != caps[i]):
            if interval_start == i - 1:
                shouts[caps[interval_start]].append(
                    f"Person in position {str(interval_start)} flip your cap!"
                )
            else:
                shouts[caps[interval_start]].append(
                    f"People in positions {str(interval_start)} through {str(i - 1)} flip your caps!"
                )
            interval_start = i

    flip_direction = "B"
    if len(shouts["F"]) < len(shouts["B"]):
        flip_direction = "F"

    return shouts[flip_direction]


def run_length_encode(message: str) -> str:
    """Optional Challenge: Run-length Encoding

    Args:
    message: a single string comprised of exactly two characters:  'F'  or 'B'

    Return:
    an encoded string which uses integers to indicate sucessive repetitions of 'F' and 'B'

    Example
    ------
    >>>run_length_encode('BFFFFFBFFFF')
    '1B5F1B4F'
    """
    encoded_msg = ""

    for c in message:
        if encoded_msg == "":
            encoded_msg += "1" + c
        elif encoded_msg[-1] == c:
            encoded_msg = encoded_msg[:-2] + str(int(encoded_msg[-2]) + 1) + c
        else:
            encoded_msg += "1" + c

    return encoded_msg


def run_length_decode(encoded_message: str) -> str:
    """Optional Challenge: Run-length Decoding

    Args:
    encoded_message: an encoded string which uses integers to indicate sucessive repetitions of 'F' and 'B'

    Return:
    a decoded string comprised of exactly two characters: 'F'  or 'B'

    Example
    ------
    >>>run_length_decode('1B5F1B4F')
    'BFFFFFBFFFF'
    """
    decoded_msg = ""

    for i in range(0, len(encoded_message), 2):
        decoded_msg += int(encoded_message[i]) * encoded_message[i + 1]

    return decoded_msg


if __name__ == "__main__":
    print(run_length_decode(run_length_encode("BFFFFFBFFFF")))  #'BFFFFFBFFFF'
