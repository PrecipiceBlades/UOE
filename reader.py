import re
import caes
class Reader(object):

    def __init__(self):
        self.weight = {}
        self.assumptions = set()
        self.argset = caes.ArgumentSet()


    def load(self,filename):
        self.filename = filename
        Reader.parse_Weight(self,self.filename)
        Reader.parse_Main_query(self,self.filename)
        Reader.parse_Proof_standard(self,self.filename)
        Reader.parse_Default_proof_standard(self,self.filename)
        Reader.parse_Assumptions(self,self.filename)
        Reader.parse_if_then(self,self.filename)
        Reader.parse_if_then_unless(self,self.filename)

    def instantiate(self):
        pass






    def hasNumbers(inputString):
    	return bool(re.search(r'\d', inputString))

    def parse_proposition(x):
        if(x[:3]=='not'):
            not_prop = x.lstrip('not')
            return caes.PropLiteral(not_prop.strip()).negate()
        else:
            return caes.PropLiteral(x)



    def parse_Weight(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif (eachline[:2] != '##' and Reader.hasNumbers(eachline)):
                mylist = eachline.split(":")
                item = float(mylist[-1].strip())
                key = mylist[0].strip()
                self.weight[key] = item
                print(self.weight)
        f.seek(0)

    def parse_Main_query(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif (eachline[:2] != '##' and eachline.find('Main query') != -1):
                mylist = eachline.split(":")
                self.main_query = mylist[-1].strip()
                print(self.main_query)
        f.seek(0)


    def parse_Proof_standard(self,f):
        proof_standard = []
        for eachline in f.readlines():
            if not eachline:
                break
            elif (eachline[:2] != '##' and eachline.find('Proof standard') != -1):
                mylist = eachline.split(":")
                prop = Reader.parse_proposition(mylist[1].strip())
                standard = mylist[-1].strip()
                prop_list = (prop,standard)
                proof_standard.append(prop_list)
                self.proof_standard = caes.ProofStandard(proof_standard)
        f.seek(0)

    def parse_Default_proof_standard(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif (eachline[:2] != '##' and eachline.find('Default proof standard') != -1):
                mylist = eachline.split(":")
                self.default_proof_standard = mylist[-1].strip()
                print(self.default_proof_standard)
        f.seek(0)

    def parse_Assumptions(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif (eachline[:2] != '##' and eachline.find('Assumption') != -1):
                mylist = eachline.split(":")
                self.assumptions.add(Reader.parse_proposition(mylist[-1].strip()))
        print(self.assumptions)
        f.seek(0)

    def parse_andprop(x):
        x = x.lstrip('If ')
        x = x.split(' and ')
        return set(map(lambda i: Reader.parse_proposition(i), x))

    def parse_orprop(x):
        x = x.split(' or ')
        return set(map(lambda i: Reader.parse_proposition(i), x))

    def parse_if_then(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif eachline[:2] != '##' and eachline.find('If') != -1 and eachline.find('unless') == -1:
                mylist = eachline.split(":")
                argument = mylist[1].strip()
                argument_list = argument.split(' then ')
                self.conclusion = Reader.parse_proposition(argument_list[1].strip())
                self.premises = Reader.parse_andprop(argument_list[0].strip())
                arg = caes.Argument(self.conclusion, premises = self.premises)
                self.argset.add_argument(arg)
                print(self.conclusion)
                print(self.premises)
        f.seek(0)

    def parse_if_then_unless(self,f):
        for eachline in f.readlines():
            if not eachline:
                break
            elif eachline[:2] != '##' and eachline.find('If') != -1 and eachline.find('unless') != -1:
                mylist = eachline.split(":")
                argument = mylist[1].strip()
                argument_list = argument.split(' unless ')
                self.exceptions = Reader.parse_orprop(argument_list[-1].strip())
                argument_list_list = argument_list[0].strip().split('then')
                self.conclusion = Reader.parse_proposition(argument_list_list[1].strip())
                self.premises = Reader.parse_andprop(argument_list_list[0].strip())
                arg = caes.Argument(self.conclusion, premises = self.premises, exceptions = self.exceptions)
                self.argset.add_argument(arg)
                print(self.conclusion)
                print(self.premises)
                print(self.exceptions)
        f.seek(0)














if __name__ == '__main__':
    caes_data = open('caesfile.txt')
    reader = Reader() # supply any init parameters
    reader.load(caes_data)
