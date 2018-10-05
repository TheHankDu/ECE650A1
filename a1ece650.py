#!/usr/bin/env python
import sys
import re


# Customized Dict Class to handle case
class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, basestring) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return '({0:.2f},{1:.2f})'.format(self.x, self.y)


# Data Processing Class
class CameraData(object):
    def __init__(self, db={}):
        self.re_coordinate = re.compile(r'\(-?[0-9 ]+,-?[0-9 ]+\)')
        self.re_street = re.compile(r'\"[a-z ]+\" ', re.I)
        self.re_street_remove = re.compile(r'\"[a-z ]+\"', re.I)
        self.db = db

        self.intersections = set([])
        self.vertices = {}
        self.edges = set([])

    def add(self, arg):
        tmp_list = []
        s_result = self.re_street.match(arg, 2)

        if s_result is not None:
            street = s_result.group().strip().strip('"')
            if not self.db.has_key(street):
                coordinate_list = []
            else:
                errprt('Invalid "add" Command', 'Street Exists in system')
                return
        else:
            errprt('Invalid "add" Command', 'Cannot find street name')
            return

        v_result = self.re_coordinate.search(arg)
        if v_result is not None:
            tmp_list.extend(self.re_coordinate.findall(arg.replace(' ', '')))
            for coordinate in tmp_list:
                x, y = coordinate.replace('(', '').replace(')', '').split(',')
                coordinate_list.append(Point(x, y))
        else:
            errprt('Invalid "add" Command', 'The format of argument {0} is invalid'.format(arg))
            return

        self.db[street] = coordinate_list

    def change(self, arg):
        tmp_list = []
        s_result = self.re_street.match(arg, 2)
        if s_result is not None:
            street = s_result.group().strip().strip('"')
            if self.db.has_key(street):
                coordinate_list = []
                v_result = self.re_coordinate.search(arg)
                if v_result is not None:
                    tmp_list.extend(self.re_coordinate.findall(arg.replace(' ', '')))
                    for coordinate in tmp_list:
                        x, y = coordinate.replace('(', '').replace(')', '').split(',')
                        coordinate_list.append(Point(x, y))
                    self.db[street] = coordinate_list
                else:
                    errprt('Invalid "change" Command', 'The format of argument {0} is invalid'.format(arg))
                    return
            else:
                errprt('Invalid "change" Command',
                       'Street {0} does NOT exist in the system or it has already been removed'.format(street))
                return
        else:
            errprt('Invalid "change" Command', 'Format for street argument in "change" command is invalid')
            return

    def remove(self, arg):
        s_result = self.re_street_remove.match(arg, 2)
        if s_result is not None:
            street = s_result.group().strip().strip('"')
            if self.db.has_key(street):
                del self.db[street]
            else:
                errprt('Invalid "remove" Command',
                       'Street {0} does NOT exist in the system or it has already been removed'.format(street))
        else:
            errprt('Invalid Argument', 'Format for "remove" argument is invalid')

    def graph(self):
        self.edges = set([])
        db_plot = {}
        tmp_ins = set([])
        self.vertices.clear()

        for sn1, pts1 in self.db.iteritems():
            db_plot[sn1] = []

            # Find intersections by looping two segments
            for i in range(len(pts1) - 1):
                add_list = []
                for sn2, pts2 in self.db.iteritems():
                    if sn1 != sn2:
                        for j in range(len(pts2) - 1):
                            i_result = self.intersection(pts1[i], pts1[i + 1], pts2[j], pts2[j + 1])
                            if i_result is not None:
                                for intersect in i_result:
                                    tmp_ins.add(intersect)
                                    if intersect != pts1[i] and intersect != pts1[i + 1]:
                                        add_list.append(intersect)

                # Add the beginning of a segment of a street that intersect with another street
                if len(add_list) > 0 or pts1[i] in tmp_ins or pts1[i + 1] in tmp_ins or ((db_plot[sn1] or [None])[-1] in tmp_ins):
                    db_plot[sn1].append(pts1[i])

                if len(add_list) >= 1:
                    add_list = list(set(add_list))
                    for pts in add_list:
                        db_plot[sn1].append(pts)

            # Add the end of a segment of a street that intersect with another street
            if (db_plot[sn1] or [None])[-1] in tmp_ins:
                db_plot[sn1].append(pts1[-1])

        index_id = 1

        for sn1, vertices in db_plot.iteritems():
            last = 0
            for index, vertex in enumerate(vertices):
                if vertex in self.vertices:
                    vertex_id = self.vertices[vertex]
                    if index > 0:
                        self.edges.add((vertex_id, last))
                    last = vertex_id
                else:
                    while index_id in self.vertices.values():
                        index_id = index_id + 1
                    self.vertices[vertex] = index_id
                    if index > 0:
                        self.edges.add((index_id, last))
                    last = index_id

        ordered_vertex = {}
        for i in range(len(self.vertices) + 1):
            for vertex, index in self.vertices.iteritems():
                if i == index:
                    ordered_vertex[i] = vertex

        outstr = 'V = {\n'
        for i, vertex in ordered_vertex.iteritems():
            if type(vertex) is not Point:
                    vertex = Point(vertex[0], vertex[1])
            outstr += '  {0}: {1}\n'.format(i, vertex)

        outstr += '}\nE = { \n'
        for edge in self.edges:
            edge_list = list(edge)
            outstr += '  <{0},{1}>,\n'.format(edge_list[0], edge_list[1])
        outstr = outstr[:-2] + '\n}'
        print(outstr)
        return

    def intersection(self, s1, d1, s2, d2):
        coordinates = [s1, d1, s2, d2]
        tmp_list = []

        x1, y1 = s1.x, s1.y
        x2, y2 = d1.x, d1.y
        x3, y3 = s2.x, s2.y
        x4, y4 = d2.x, d2.y

        x_range = (max(min(x1, x2), min(x3, x4)), min(max(x1, x2), max(x3, x4)))
        y_range = (max(min(y1, y2), min(y3, y4)), min(max(y1, y2), max(y3, y4)))

        if x1 != x2 and x3 != x4:
            m1 = (y2 - y1) / (x2 - x1)
            m2 = (y4 - y3) / (x4 - x3)
            b1 = y1 - m1 * x1
            b2 = y3 - m2 * x3
            if m1 is m2 and b1 is b2:
                for coord in coordinates:
                    if x_range[0] <= coord.x <= x_range[1] and y_range[0] <= coord.y <= y_range[1]:
                        tmp_list.append(coord)
                return tmp_list
        elif x1 is x2 and x3 is x4:
            tmp_list = []
            for coord in coordinates:
                if y_range[0] <= coord.y <= y_range[1]:
                    tmp_list.append(coord)
            return tmp_list

        x_num = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))
        x_den = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        y_num = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        y_den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if x_den != 0 or y_den != 0:
            x_coord = x_num / x_den
            y_coord = y_num / y_den
        else:
            return None

        if x_coord < x_range[0] or x_coord > x_range[1] or y_coord < y_range[0] or y_coord > y_range[1]:
            return None

        else:
            return [(x_coord, y_coord)]

    def is_vertex(self, l1, l2, int_sec):
        x1, y1 = l1.x, l1.y
        x2, y2 = l2.x, l2.y
        xi, yi = int_sec.x, int_sec.y

        if x1 == x2:
            if xi == x1 and max(y1, y2) >= yi >= min(y1, y2):
                return True
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            if (yi == m * xi + b and max(x1, x2) >= xi >= min(x1, x2) and max(y1, y2) >= yi >= min(y1,
                                                                                                   y2)):
                return True
        return False


# Global Function
# act like exception

def errprt(msg, reason):
    sys.stderr.write('Error: {0}. Possible Reason: {1}\n'.format(msg, reason))


def initialization():
    db = CaseInsensitiveDict({})
    data = CameraData(db)
    return data


def main_loop(data):
    is_quit = False
    while not is_quit:
        command = sys.stdin.readline().strip()
        if command == '':
            break
        cmd_list = command.split(' ')

        if (cmd_list[0] == 'a') and (len(cmd_list) > 2):
            data.add(command)
        elif (cmd_list[0] == 'c') and (len(cmd_list) > 2):
            data.change(command)
        elif cmd_list[0] == 'r':
            data.remove(command)
        elif (cmd_list[0] == 'g') and (len(cmd_list) == 1):
            data.graph()
        elif cmd_list[0] == 'q':
            is_quit = True
        else:
            errprt('Command [{0}] is not valid'.format(cmd_list), 'Wrong command name or incorrect arguments')
    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    data = initialization()
    try:
        main_loop(data)
    except KeyboardInterrupt:
        sys.exit(0)
