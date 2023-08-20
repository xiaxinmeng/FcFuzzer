import ast
import ast_analysis 
import itertools
import ast_transform
import os


builtins = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']


def transSSA(var):
	newvar = set()
	if var:
		var =list(var)
		var.sort(key = lambda x:(x[1],x[2]),reverse = False)

		uniquename ={}

		for v in var:
			varName = v[0]

			if v[3] == "Store" and varName in uniquename.keys():
				uniquename[varName] = uniquename[varName] + 1
				newvarName = varName +"_%s"%str(uniquename[varName])
				newvar.add((newvarName,v[1],v[2],v[3]))
			else:
				uniquename[varName] = 0
				newvar.add(v)
	return newvar

def fliter_User_define_func(call,func,var):
	newcall = set()
	for c in call:
		call_name = c[0]
		call_lineno = c[1]
		is_user_define = False
		for f in func:
			func_name = f[0]
			func_lineno = f[1]
			if call_name == func_name and call_lineno > func_lineno:
				is_user_define = True
		if is_user_define:
			newcall.add(c)
	return newcall


def add_buildinfunc_var(callname,calldic,var):
	for c in calldic.keys():
		if c not in callname:
			for item in calldic[c]:
				var.add(item)

	return var





def find_node_for_range(holes,trange):
	rangenode = {}
	for item in trange.keys():
		name = item[0]
		lineno = item[1]
		col_offset= item[2]
		para = item[3]
		mark = item[4]
		startPos = int(trange[item][0])
		endPos = int(trange[item][1])
		key = (name,lineno,col_offset,para,mark)
		rangenode[key] = [[startPos,endPos],set()]

		for h in holes:
			holelineno = h[1]
			if holelineno > startPos-1 and holelineno < endPos + 1:
				rangenode[key][1].add(h)
	return rangenode



def scopePartition(holes,classname,funcname):
	classnode = find_node_for_range(holes,classname)
	funcnode = find_node_for_range(holes,funcname)

	globalname = {('global',0,10000,0,'global'):[0,10000]}
	globalnode = find_node_for_range(holes,globalname)
	# print("........",classnode,funcnode,globalnode)

	scopedic = {}
	scopedic.update(classnode)
	scopedic.update(funcnode)
	scopedic.update(globalnode)

	tempdic = scopedic
	for key in scopedic:
		for tem in tempdic:
			scope_start_pos = scopedic[key][0][0]
			scope_end_pos = scopedic[key][0][1]
			tem_start_pos = tempdic[tem][0][0]
			tem_end_pos = tempdic[tem][0][1]
			if scope_start_pos < tem_start_pos and scope_end_pos >= tem_end_pos:
				scopedic[key][1] = scopedic[key][1] - tempdic[tem][1]
	return scopedic




def selectHole(smNum,holes):
	# print(holes)
	holelist = []
	for hole in holes:
		holelineno = hole[1]
		if holelineno in smNum:
			holelist.append(hole)
	return holelist





def ToListSet(iterable):
    rlist = []

    for item  in iterable:

        slist = []
        for k in item:

            if isinstance(k,list):
                slist =slist + k
            else:
                slist.append(k)
        rlist.append(slist)


    # print(rlist)
    return rlist



def combine_func_call(hole, define_cand, scopedic):
	newdefin_cand = set()

	for scope in scopedic:
		if scope[4] != "global" and scope[4] != "class":
			if hole[1] > scope[1]:
				if scope[3] != 0:
					elist = ToListSet(itertools.product(define_cand,repeat = scope[3]))
					# print(elist)
					for item in elist:
						newdefin_cand.add((scope[0],tuple(item)))
				else:
					newdefin_cand.add((scope[0],()))
	out_cand = newdefin_cand | define_cand
	return out_cand



def rankEnum(enum):
	enum = sorted(enum,key=lambda x:(x[1],-x[2]))
	return enum


def add_hole_to_enum(candiset,hole, single_enum_list):
	newholelist = []
	for can in candiset:
		newholelist.append((can,hole[1],hole[2],hole[3]))

	newenumlist = []
	if single_enum_list:
		for h in newholelist:
			temp = []
			for item in single_enum_list:
				temp.append(item)
			temp.append(h)
			newenumlist.append(temp)

	else:
		for h in newholelist:
			newenumlist.append([h])
	# print("nn",newenumlist)
	return newenumlist

def get_enum( enum_list, holelist,scopedic,startline,funcargs):
	old_enum = enum_list
	newenumlist = []
	# for single_enum_list in enum_list:
	
	holelist = rankEnum(holelist)
	# print("holelist.....",holelist)

	all_candidate = 0
	enum_time = 0

	for hole in holelist:
		# print("hole..",hole)
		newenumlist = []
		scopepos = []
		define_cand = set()

		for scope in scopedic:
			scope_start = scopedic[scope][0][0]
			scope_end = scopedic[scope][0][1]
			scopeset = scopedic[scope][1]
			holeline = hole[1]
			if holeline > scope_start and holeline <= scope_end:
				for item in scopeset:
					if item[1] <=  startline:
						scopepos.append(item)
				if scope in funcargs:
					# print("sssssssss",set(funcargs[scope]))
					# print("arge",funcargs[scopeset])
					define_cand = define_cand| set(funcargs[scope])



		if enum_list:

			for single_enum_list in enum_list:
				# print(single_enum_list,scopepos)
				new_define_cand = set()
				new_define_cand = new_define_cand | define_cand
				for enum in single_enum_list:
					for s in scopepos:
						if s[1] == enum[1] and s[2] == enum[2]:
							if enum[0] in builtins:
								new_define_cand.add(enum[0])
							new_define_cand.add(enum[0])



				if hole[3] == 'Store':
					sdefine_cand =set()
					sdefine_cand = sdefine_cand | new_define_cand
					sdefine_cand.add(hole[0])
					temp = set()
					for item in sdefine_cand:
						if not isinstance(item,tuple):
							temp.add(item)
					sdefine_cand = temp


					newenumlist = newenumlist + add_hole_to_enum(sdefine_cand,hole, single_enum_list)
					all_candidate = all_candidate + len(sdefine_cand)
					enum_time = enum_time + 1
					# print(all_candidate)

				if hole[3] == 'Load':
					ldefine_cand =set()
					ldefine_cand = ldefine_cand | new_define_cand
					# print("b",ldefine_cand)
					if hole[0] in builtins:
						ldefine_cand.add(hole[0])
					ldefine_cand = combine_func_call(hole, ldefine_cand, scopedic)
					# print("A",ldefine_cand)
					# print("l",ldefine_cand,hole,single_enum_list)	
					# print(newenumlist)
					newenumlist = newenumlist + add_hole_to_enum(ldefine_cand,hole, single_enum_list)
					all_candidate = all_candidate + len(ldefine_cand)
					enum_time = enum_time + 1


		else:
			# define_cand = define_cand | set(scopepos)
			if hole[3] == 'Store':
				define_cand.add(hole[0])
				# print("s",hole,define_cand)
				newenumlist = add_hole_to_enum(define_cand,hole, enum_list)
				all_candidate = all_candidate + len(define_cand)
				enum_time = enum_time + 1
				# print(all_candidate)
			if hole[3] == 'Load':
				# print("l",hole,define_cand)
				define_cand.add(hole[0])	
				define_cand = combine_func_call(hole, define_cand, scopedic)
				# print("l",hole,define_cand)			
				newenumlist = add_hole_to_enum(define_cand,hole, enum_list)
				all_candidate = all_candidate + len(define_cand)
				# print(all_candidate)
				enum_time = enum_time + 1

		enum_list = newenumlist

	if not newenumlist:
		newenumlist = old_enum

	return newenumlist,all_candidate,enum_time




def gen_tup_sgs(id_name,strict_grow_str,strict_grow_str_dic, maxnum):
	# print(id_name)
	cname =  id_name[0]
	if not id_name[1]:
		#foo()
		strict_grow_str = strict_grow_str + cname
		return strict_grow_str,strict_grow_str_dic,maxnum

	else:
		strict_grow_str = strict_grow_str + cname
		for item in id_name[1]:
			if isinstance(item, str):
				if item not in strict_grow_str_dic.keys():
					maxnum = maxnum + 1
					strict_grow_str_dic[item] = maxnum
				strict_grow_str = strict_grow_str + str(strict_grow_str_dic[item])
			if isinstance(item,tuple):
				# strict_grow_str = strict_grow_str + cname
				strict_grow_str,strict_grow_str_dic,maxnum = gen_tup_sgs(item,strict_grow_str,strict_grow_str_dic, maxnum)
		return	strict_grow_str,strict_grow_str_dic,maxnum

def reduce_isomorphic(enumlist):

	newenumlist = [] 
	strict_grow_str_set = set()
	
	for enum in enumlist:
		strict_grow_str_dic = {}

		strict_grow_str = ""
		maxnum = 0
		for node in enum:
			id_name = node[0]
			if isinstance(id_name,str):
				if id_name not in strict_grow_str_dic.keys():
					maxnum = maxnum + 1
					strict_grow_str_dic[id_name] = maxnum 
				strict_grow_str = strict_grow_str + str(strict_grow_str_dic[id_name])
			if isinstance(id_name,tuple):
				strict_grow_str,strict_grow_str_dic,maxnum = gen_tup_sgs(id_name,strict_grow_str,strict_grow_str_dic, maxnum)


		
		if strict_grow_str not in strict_grow_str_set:
			# print(enum,strict_grow_str)
			newenumlist.append(enum)
			strict_grow_str_set.add(strict_grow_str)

	return newenumlist





def conjunt(tup ):
	# print(tup)
	fc = ""
	cname = tup[0]

	fc = fc +  cname + "("
	# print(fc)
	if not tup[1]:
		fc = fc 
	else:
		i = 0
		for item in tup[1]:
			if not item:
				fc = fc +  "("+")"

			elif isinstance(item,str):
				if i < len(tup[1])-1:
					fc = fc + item + ','
					i = i + 1
				else:
					fc = fc +item 
			elif isinstance(item,tuple):
				# print(item)
				if i < len(tup[1])-1:

					fc =fc+conjunt(item)+","
					i = i + 1
				else:
					fc =fc+conjunt(item)

	fc = fc+")"
	return fc



