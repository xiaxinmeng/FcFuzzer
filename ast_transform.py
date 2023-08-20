import ast

class Transformer(ast.NodeTransformer):
    def __init__(self,changelist,callname):
        self.changelist = changelist
        self.callname = callname
        self.calllist = []
        self.namedic = {}
        self.calldic = {}



    def handle_call(self):
        for item in self.callname:
            self.calllist.append((item[1],item[2]))

        for item in self.changelist:
            postup = (item[1],item[2])
            if postup in self.calllist:
              self.calldic[postup] = item[0]

            else:
              self.namedic[postup] =item[0]



    def visit_Call(self, node): 

        if isinstance(node.func, ast.Attribute):
            pass
        else:

          postup = (node.lineno,node.col_offset)
          if postup in self.calldic:

            node = ast.parse(self.calldic[postup]).body[0].value


        self.generic_visit(node)
        return node

    def visit_Name(self, node): 
        self.generic_visit(node)  

        postup = (node.lineno,node.col_offset)

        if postup in self.namedic.keys():

          if "(" in self.namedic[postup]:
            # print(postup)
            node = ast.parse(self.namedic[postup]).body[0].value
          else:
            node.id = self.namedic[postup]

        return node


def transform(translist,myast):
    trans = Transformer(translist)
    newast = trans.visit(myast)
    program = ast.unparse(newast)
    return program


