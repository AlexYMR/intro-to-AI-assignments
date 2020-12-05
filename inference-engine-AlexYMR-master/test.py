import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
    # Assert starter facts
    file = 'statements_kb3.txt'
    data = read.read_tokenize(file)
    KB = KnowledgeBase([], [])
    for dtype, item in data:
        if dtype == read.FACT or dtype == read.RULE:
            KB.kb_assert(item)

    # KB demonstration
    # Ask for one of the starter facts
    print "Starting basic KB demonstration"
    _, ask1 = read.parse_input("fact: (goodman ?x)")
    print " Asking if", ask1
    answer = KB.kb_ask(ask1)
    pprint_justification(answer)
    print KB
    
def pprint_justification(answer):
    """Pretty prints (hence pprint) justifications for the answer.
    """
    if not answer: print 'Answer is False, no justification'
    else:
        print '\nJustification:'
        for i in range(0,len(answer.list_of_bindings)):
            # print bindings
            print answer.list_of_bindings[i][0]
            # print justifications
            for fact_rule in answer.list_of_bindings[i][1]:
                pprint_support(fact_rule,0)
        print

def pprint_support(fact_rule, indent):
    """Recursive pretty printer helper to nicely indent
    """
    if fact_rule:
        print " "*indent, "Support for", 

        if isinstance(fact_rule, Fact):
            print fact_rule.statement
        else:
            print fact_rule.lhs, "->", fact_rule.rhs

        if fact_rule.supported_by:
            for pair in fact_rule.supported_by:
                print " "*(indent+1), "support option"
                for next in pair:
                    pprint_support(next, indent+2)



if __name__ == '__main__':
    main()
