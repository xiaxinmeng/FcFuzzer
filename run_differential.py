import os
import ast
import ast_analysis
import algorithm as ga
import ast_transform
from wrapt_timeout_decorator import timeout

# print(os.getcwd())


@timeout(90,use_signals = False)
def run(inputfile):

	rootname = inputfile.split("/dataset/")[0]
	dirname = "/".join(inputfile.split("/dataset/")[1].split('/')[:-1])
	fname = inputfile.split(".py")[0].split('/')[-1]
	dirpath = rootname + "/log/"+dirname
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)
	

	logfilename = dirpath + '/'+ fname + "_log.txt"
	if os.path.exists(logfilename):
		os.remove(logfilename)

	logfile = open(logfilename, 'a') 

	logfile.write("Seed file: %s\n"%inputfile)
	print(inputfile)

	f= open(inputfile,'r').read()


	myast = ast.parse(f)
	# print(ast.dump(myast))
	astvisitor = ast_analysis.CellVisitor()
	astvisitor.visit(myast)
	# print("All name:",astvisitor.allname,'\n')
	# print("call:",astvisitor.callname,'\n')
	# print("func:",astvisitor.funcRange,'\n')
	# print("class:",astvisitor.classRange,'\n')
	# print("attr name:",astvisitor.attrname,'\n')
	# print("func call arguments:",astvisitor.callarg,'\n')
	funcargs = astvisitor.funcargs


	classname = astvisitor.classRange
	funcname =astvisitor.funcRange
	callname = astvisitor.callname
	calldic = astvisitor.calldic
	var = astvisitor.allname - astvisitor.attrname - callname 


	callname = ga.fliter_User_define_func(callname,funcname,var)
	# print(callname)

	var = ga.add_buildinfunc_var(callname,calldic,var)


	vload = 0
	vstore = 0
	for v in var:
		v_status = v[3]
		if v_status == "Load":
			vload = vload + 1
		else:
			vstore = vstore + 1

	varload = []
	varstore =[]
	vload = 0
	vstore = 0
	for v in var:
		v_status = v[3]
		if v_status == "Load":
			vload = vload + 1
			varload.append(v)
		else:
			vstore = vstore + 1
			varstore.append(v)
	# varstore = ga.transSSA(varstore)
	# var = set(varstore) | set(varload)
	# print(var)


	logfile.write("Number of function: %s\n"%len(funcname))
	print("Number of function:", len(funcname))

	logfile.write("Load hole: %s\n"%(vload+len(callname)))
	print("Load hole:",vload+len(callname))


	logfile.write("Store hole: %s\n"%vstore)
	print("Store hole:",vstore)


	logfile.write("Function call hole: %s\n"%len(callname))
	# print("Function call hole:", len(callname))

	# print("call hole:",len(callname))

	# holes = var | callname
	holes = var 
	# print(holes)


	scopedic = ga.scopePartition(holes,classname,funcname)


	# for key in scopedic:
	# 	print(key,scopedic[key])

	enumlist = []


	f= open(inputfile,'r').readlines()
	code = ""
	linecount = 0
	smNum = []
	derive_time = 0

	file_line = 0
	all_candidate =0
	enum_time = 0 
	before_reduct = 0
	after_reduct = 0

	for line in f:
		# print(line)
		# if line != "\n" and not line.startswith("#"):
		file_line = file_line + 1
		linecount = linecount + 1
		code =code + line

		# # print("code\n",code)

		try:
			myast = ast.parse(code)
			# print(ast.dump(myast))
		except:
			smNum.append(linecount)
			# print("error..........")
		else:
			
			smNum.append(linecount)
			# print(smNum)
			holelist = ga.selectHole(smNum,holes)
			# print(holelist)

			startline = smNum[0]
			enumlist,a_cand,e_time = ga.get_enum( enumlist, holelist,scopedic,startline,funcargs)
			# print(cdate)
			all_candidate = all_candidate+ a_cand
			enum_time = enum_time + e_time
			before_reduct = before_reduct + len(enumlist)
			# print("Before reduction: ",len(enumlist))
			enumlist = ga.reduce_isomorphic(enumlist)

			after_reduct = after_reduct + len(enumlist)
			# print("After reduction: ",len(enumlist))
			smNum = []
			if line != "\n" and not line.startswith("#"):
				derive_time = derive_time + 1


	# print("Before reduction: ",before_reduct)
	# print("After reduction: ",after_reduct)

	if enum_time !=0:
		# print(all_candidate)
		logfile.write("Average candidate: %s\n"%(all_candidate/enum_time))
		# print("Average candidate:", all_candidate/enum_time)
	else:
		logfile.write("Average candidate: 0\n")
		# print("Average candidate:",0)


	logfile.write("Enum_time: %s\n"%enum_time)
	# print("Enum_time:",enum_time)

	logfile.write("Derive_time: %s\n"%derive_time)
	# print("Derive_time:", derive_time)

	logfile.write("Lines of code: %s\n"%file_line)
	print("Lines of code",file_line)


	logfile.write("Number of enumerated program: %s\n"%(len(enumlist)))	
	print("The number of generated programs:",(len(enumlist)))
	return enumlist,callname


@timeout(30,use_signals = False)
def test_file(interpreter, program,sourcepath, j):
    rt = sourcepath.split("/dataset/")[0]
    dr = "/".join(sourcepath.split("/dataset/")[1].split("/")[:-1])
    fl = sourcepath.split("/dataset/")[1].split('/')[-1]

    rundir = rt + "/dataset/"+dr
    savepath = rundir+"/temp.py"
    open(savepath,'w').write(program)


    s = os.system("cd %s;%s %s"%(rundir, interpreter, savepath ))

    if s !=0 and s!=256:
        name = sourcepath.split(".py")[0].split('/')[-1]
        dirname = rt+"/error/" + dr
        dest = dirname + "/"+ "%s__%s.py"%(str(name),str(j))



        if not os.path.exists(dirname):
            os.makedirs(dirname)


        open( dest,'w').write(program)
        j=j+1
        open('log.txt','a').write("%s_%s=========%s\n"%(name,j,s))

    return j


@timeout(7200)
def trans_program(interpreter, interpreter_base, inputfile, enumlist,callname):


# # the target Python interpreter
# 	interpreter =  'rustpython'
# # the reference Python interpreter
# 	interpreter_base = "python3.9.0"


	j = 0
	f= open(inputfile,'r').read()

	try:
		j = test_file_differential(interpreter, interpreter_base, f,inputfile, j)
		# print(j)
	except:
		pass


	k = 0
	for enum in enumlist:

		k = k + 1

		print("\n\n\n", "The execution of the %sth test program, %s test programs are left."%(k, len(enumlist) - k),"\n______________")



		changelist = []
		for item in enum:
			if isinstance(item[0],str):
				changelist.append(item)
			if isinstance(item[0],tuple):
				
				fcall = ga.conjunt(item[0])

				changelist.append((fcall,item[1],item[2],item[3]))
		

		f= open(inputfile,'r').read()


		myast = ast.parse(f)
		# print("!!!")
		trans = ast_transform.Transformer(changelist,callname)
		trans.handle_call()
		newast = trans.visit(myast)
		program = ast.unparse(newast)
		print(program,"\n","\n","\n")

		try:
			j = test_file_differential(interpreter, interpreter_base, program,inputfile, j)
		except:
			pass

		


@timeout(30,use_signals = True)
def test_file_differential(interpreter, interpreter_base, program,sourcepath, j):

    rt = sourcepath.split("/dataset/")[0]
    dr = "/".join(sourcepath.split("/dataset/")[1].split("/")[:-1])
    fl = sourcepath.split("/dataset/")[1].split('/')[-1]

    rundir = rt + "/dataset/"+dr
    savepath = rundir+"temp.py"
    # print(program)
    open(savepath,'w').write(program)

    print("Behaviors on %s:"%interpreter)    
    s = os.system("cd %s;%s %s"%(rundir, interpreter, savepath ))
    print("Behaviors on %s:"%interpreter_base) 
    s1 = os.system("cd %s;%s %s"%(rundir, interpreter_base, savepath ))

    # print(s,s1)
    if s !=s1:
        name = sourcepath.split(".py")[0].split('/')[-1]
        dirname = rt+"/error/" + dr
        dest = dirname + "/"+ "%s__%s.py"%(str(name),str(j))
        # dirname  = sourcepath.split(".py")[0].split('/')[-2]


        if not os.path.exists(dirname):
            os.makedirs(dirname)


        open( dest,'w').write(program)
        j=j+1
        open('log.txt','a').write("%s_%s=========%s\n"%(name,j,s))

    return j



import datetime



tdir = os.getcwd() + "/dataset"





#### Set your baseline interpreter and the target interpreter.
interpreter_base =  os.getcwd() + '/Python3.9.0/python'
interpreter_target = "rustpython"




for root,dirs, files in os.walk(tdir):
	for file in files:
		# print(root,file)
		path = root+ "/"+file
		if path.endswith(".py"): 
			filename = path.split(".py")[0].split('/')[-1]
			dirname = path.split(".py")[0].split('/')[-2] 
			# print(path)
			if filename != dirname and filename != "temp":
				print("Enumerating",path)
				starttime = datetime.datetime.now()
				try:
					enumlist,callname = run(path)


					#if len(enumlist) > 10000:
					#	enumlist = enumlist[:10000]

					trans_program(interpreter_target, interpreter_base, path,enumlist,callname)

					logfilename =path.split("/dataset/")[0]+"/log"+  "/".join(path.split("/dataset/")[1].split('/')[:-1]) + '/'+ path.split(".py")[0].split('/')[-1] + "_log.txt"
					print("....................",logfilename)
					endtime = datetime.datetime.now()
					open(logfilename,'a').write("Total time: %s"%(endtime - starttime))
					print((endtime - starttime))
				except:
					pass



print("All seed programs have been processed...........")


