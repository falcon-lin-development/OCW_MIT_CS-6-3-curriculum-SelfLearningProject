import rubik
from collections import deque


class d(dict):
    def __str__(self):
        out = ""
        for key, value in self.items():
            out += "{0}: {1},\n".format(key, value)
        return "{" + out[:-2] + "}"
    __repr__ = __str__


def shortest_path(start, end, verbose=0, termination_check=True):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    #  Set up
    dict_from_start = d()
    dict_form_end = d()
    agenda_start = Queue()
    agenda_end = Queue()
    operations = rubik.quarter_twists

    agenda_start.put_elt(SearchNode((start, None), None))
    agenda_end.put_elt(SearchNode((end, None), None))
    flip = True
    if termination_check: counter = 0

    if verbose:
        print "===================================================================================="
        print "start: {0}".format(start)
        print "end: {0}".format(end)
        print "State: {0}".format("SetUp")
        print "dict_start: {0}".format(dict_from_start)
        print "dict_end: {0}".format(dict_form_end)
        print "agenda_start: {0}".format(agenda_start)
        print "agenda_end: {0}".format(agenda_end)
        print "===================================================================================="

    while not agenda_start.is_empty() and not agenda_end.is_empty():
        if verbose:
            print "===================================================================================="
            print "State: {0}".format("InLoop_s")
            if flip:
                print "At Start"
                print "dict_start: {0}".format(dict_from_start)
                print "agenda_start: {0}".format(agenda_start)
            if not flip:
                print "At End"
                print "dict_end: {0}".format(dict_form_end)
                print "agenda_end: {0}".format(agenda_end)
            print "calculating..."

        # Flipping style
        if flip:
            _dict = dict_from_start
            _agenda = agenda_start
            _other = dict_form_end
        else:
            _dict = dict_form_end
            _agenda = agenda_end
            _other = dict_from_start
        # do one level permutation
        current = _agenda.pop_elt()
        _dict[current.name] = current
        children = [SearchNode((rubik.perm_apply(op, current.value), op), current) for op in operations]
        # dynamic programming
        for child in children:
            if child.name not in _dict:
                _agenda.put_elt(child)

        if verbose:
            print "State: {0}".format("InLoop_e")
            if flip:
                print "dict_start: {0}".format(dict_from_start)
                print "agenda_start: {0}".format(agenda_start)
            else:
                print "dict_end: {0}".format(dict_form_end)
                print "agenda_end: {0}".format(agenda_end)
            print "===================================================================================="

        # Termination Check
        if termination_check:
            if len(_dict) >= 100 and counter == 0:
                counter += 1
                print "100"
            elif len(_dict) >= 1000 and counter == 1:
                counter += 1
                print "1000"
            elif len(_dict) >= 10000 and counter == 2:
                counter += 1
                print "10000"
            elif len(_dict) >= 100000 and counter == 3:
                counter += 1
                print "100000"
            elif len(_dict) >= 1000000 and counter == 4:
                counter += 1
                print "1000000"
            # elif len(_dict) >= 2000000 and counter == 5:
            #     counter += 1
            #     print "2000000"
            # elif len(_dict) >= 2000000 and counter == 6:
            #     counter += 1
            #     print "3000000"
            if len(_dict) >= 3674160//2:
                break

        # Flip
        flip = not flip
        # Terminate condition
        if verbose: print "check Termination.........."
        if current.name in _other:
            from_start = dict_from_start[current.name].get_path()
            from_end = [rubik.perm_inverse(op) for op in reversed(dict_form_end[current.name].get_path())]
            if verbose: print "Result: {0}".format([rubik.quarter_twists_names[op] for op in from_start+from_end])
            return from_start + from_end
        if verbose: print "Done checking."

    if verbose: print "No solution"
    return None


class SearchNode(object):
    def __init__(self, values, parent):
        self.name = rubik.perm_to_string(values[0])
        self.value, self.op = values
        self.parent = parent
        if parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0

    def get_parent_name(self):
        if self.parent is None:
            return "None"
        else:
            return self.parent.name

    def get_path(self):
        if self.op is None:
            return []
        else:
            return self.parent.get_path() + [self.op]

    def get_path_name(self):
        if self.op is None:
            return []
        else:
            return self.parent.get_path_name() + [rubik.quarter_twists_names[self.op]]

    def get_op_name(self):
        if self.op is None:
            return "None"
        else:
            return rubik.quarter_twists_names[self.op]

    def __str__(self):
        return '<{0}, {1}>'.format(self.get_path_name(), self.level)
    __repr__ = __str__


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def get_elt(self):
        pass

    def put_elt(self):
        pass


class Queue(PriorityQueue):
    """First In First Out"""

    def __init__(self):
        self.count = 0
        self.queue = deque()

    def pop_elt(self):
        self.count += 1
        return self.queue.popleft()

    def put_elt(self, elt):
        self.count -= 1
        return self.queue.append(elt)

    def is_empty(self):
        return not bool(self.count)

    def __str__(self):
        out = ""
        for i in self.queue:
            out += i.__str__() + ",\n"
        return "(" + out[:-2] + " )"
    __repr__ = __str__
