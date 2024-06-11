import random

from maadb.loader.loaderRiak import generateAllPatient

l = generateAllPatient().keys()

# Lista di tuple di esempio
my_list_of_tuples = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e'), (6, 'f'), (7, 'g'), (8, 'h'), (9, 'i'), (10, 'j'),
                     (11, 'k'), (12, 'l'), (13, 'm'), (14, 'n'), (15, 'o'), (16, 'p'), (17, 'q'), (18, 'r'), (19, 's'), (20, 't'),
                     (21, 'u'), (22, 'v'), (23, 'w'), (24, 'x'), (25, 'y'), (26, 'z'), (27, 'aa'), (28, 'bb'), (29, 'cc'), (30, 'dd'),
                     (31, 'ee'), (32, 'ff'), (33, 'gg'), (34, 'hh'), (35, 'ii'), (36, 'jj'), (37, 'kk'), (38, 'll'), (39, 'mm'), (40, 'nn'),
                     (41, 'oo'), (42, 'pp'), (43, 'qq'), (44, 'rr'), (45, 'ss'), (46, 'tt'), (47, 'uu'), (48, 'vv'), (49, 'ww'), (50, 'xx'),
                     (51, 'yy'), (52, 'zz'), (53, 'aaa'), (54, 'bbb'), (55, 'ccc'), (56, 'ddd'), (57, 'eee'), (58, 'fff'), (59, 'ggg'), (60, 'hhh'),
                     (61, 'iii'), (62, 'jjj'), (63, 'kkk'), (64, 'lll'), (65, 'mmm'), (66, 'nnn'), (67, 'ooo'), (68, 'ppp'), (69, 'qqq'), (70, 'rrr'),
                     (71, 'sss'), (72, 'ttt'), (73, 'uuu'), (74, 'vvv'), (75, 'www'), (76, 'xxx'), (77, 'yyy'), (78, 'zzz'), (79, 'aaaa'), (80, 'bbbb'),
                     (81, 'cccc'), (82, 'dddd'), (83, 'eeee'), (84, 'ffff'), (85, 'gggg'), (86, 'hhhh'), (87, 'iiii'), (88, 'jjjj'), (89, 'kkkk'), (90, 'llll'),
                     (91, 'mmmm'), (92, 'nnnn'), (93, 'oooo'), (94, 'pppp'), (95, 'qqqq'), (96, 'rrrr'), (97, 'ssss'), (98, 'tttt'), (99, 'uuuu'), (100, 'vvvv')]

# Numero di elementi da estrarre
num_elements_to_extract = 50

# Assicurati che la lista abbia abbastanza elementi
if len(my_list_of_tuples) >= num_elements_to_extract:
    random_elements = random.sample(my_list_of_tuples, num_elements_to_extract)
else:
    print(f"La lista ha solo {len(my_list_of_tuples)} elementi, quindi tutti gli elementi saranno selezionati.")
    random_elements = my_list_of_tuples

print(random_elements)
