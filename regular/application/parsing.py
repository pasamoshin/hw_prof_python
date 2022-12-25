from re import sub


def mod_fio(data):
    for d in data:
        if not d[2]:
            name_surname = d[1].split(' ')
            if len(name_surname) > 1:
                i = 1
                for n in name_surname:
                    d[i] = n
                    i += 1
                continue
            name_surname = d[0].split(' ')
            if len(name_surname) > 1:
                i = 0
                for n in name_surname:
                    d[i] = n
                    i += 1
    return data


def change_number(data):
    num_pattern = r'(\+7|8)\s*\(?(\d{3})\)?\-?\s*?(\d{3})\-?(\d{2})\-*(\d{2})((\s*?)\(?(\доб.)\s(\d*)\)?)?'
    num_pattern_mod = r"+7(\2)\3-\4-\5\7\8\9"
    for d in data:
        d[5] = sub(num_pattern, num_pattern_mod, d[5])
    return data


def remove_duplicates(list_):
    d = dict()
    for i in list_:
        d[i[0], i[1]] = i[2:]

    for i in list_:
        fi = (i[0], i[1])
        if fi in d:
            list_d = d[fi]
            list_l = i[2:]
            if list_d != list_l:
                index = 0
                new_list = list()
                for v in list_d:
                    if v != '':
                        new_list.append(v)
                    else:
                        new_list.append(list_l[index])
                    index += 1
                    if index > 4:
                        break
                d[fi] = new_list

    res_list = list()
    for k, v in d.items():
        res_list.append([*k, *v])
    return res_list
