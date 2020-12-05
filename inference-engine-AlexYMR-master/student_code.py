import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # //--
        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:
                fact_or_rule = self.facts[self.facts.index(fact_or_rule)]
                if not fact_or_rule.asserted:
                    return #deemed not an asserted fact, so deny retraction
                    
                def recursiveRetract(fact_rule):
                    if len(fact_rule.supports_facts) > 0 or len(fact_rule.supports_rules) > 0:
                        if len(fact_rule.supports_facts) > 0:
                            listCopy = fact_rule.supports_facts[:] #prevents list mutation errors
                            for f in listCopy:
                                print("now on " + f.name)
                                recursiveRetract(f)
                                print("now out from " + f.name)
                        if len(fact_rule.supports_rules) > 0:
                            listCopy = fact_rule.supports_rules[:] #prevents list mutation errors
                            for r in listCopy:
                                print("now on " + r.name)
                                recursiveRetract(r)
                                print("now out from " + r.name)
                        if isinstance(fact_rule,Fact):
                            if len(fact_rule.supported_by) > 0:
                                for fr in fact_rule.supported_by:
                                    print("removing..." + fact_rule.name + " from " + fr[0].name)
                                    fr[0].supports_facts.remove(fact_rule)
                                fact_rule.supported_by.clear()
                            if not fact_rule.asserted:
                                self.facts.remove(fact_rule) #remove fact
                        elif isinstance(fact_rule,Rule):
                            if len(fact_rule.supported_by) > 0:
                                for fr in fact_rule.supported_by:
                                    print("removing..." + fact_rule.name + " from " + fr[0].name)
                                    fr[0].supports_rules.remove(fact_rule)
                                fact_rule.supported_by.clear()
                            self.rules.remove(fact_rule) #remove rule
                    else:
                        # if another supporting fact found, don't remove, otherwise, remove...?
                        # the way our KB is built, supported_by can only have ONE fact/rule pair, so remove automatically?
                        if isinstance(fact_rule,Fact):
                            if len(fact_rule.supported_by) > 0:
                                for fr in fact_rule.supported_by:
                                    print("removing..." + fact_rule.name + " from " + fr[0].name)
                                    fr[0].supports_facts.remove(fact_rule)
                                fact_rule.supported_by.clear()
                            if not fact_rule.asserted:
                                self.facts.remove(fact_rule) #remove purely dependent fact
                        elif isinstance(fact_rule,Rule):
                            if len(fact_rule.supported_by) > 0:
                                for fr in fact_rule.supported_by:
                                    print("removing..." + fact_rule.name + " from " + fr[0].name)
                                    fr[0].supports_rules.remove(fact_rule)
                                fact_rule.supported_by.clear()
                            self.rules.remove(fact_rule)

                recursiveRetract(fact_or_rule)

                # how should inconsistency be dealt with?
                # 1) go through supported_by and remove that it supports *this* fact (current approach -- basically ignore inconsistency)
                # OR 2) go through supported_by and remove its supports entirely down to the root
                # OR 3) deny the retraction

someIDX = 0
anotherIDX = 0
class InferenceEngine(object):
    
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # //--
        bindings = match(rule.lhs[0],fact.statement)
        if bindings:
            # print(str(bindings))
            if len(rule.lhs) == 1:
                global someIDX
                newFact = Fact(instantiate(rule.rhs,bindings),[[fact],[rule]])
                newFact.name = "fact_" + str(someIDX)
                someIDX+=1
                fact.supports_facts.append(newFact)
                rule.supports_facts.append(newFact)
                kb.kb_assert(newFact)
            else:
                idx = -1
                for stmnt in rule.lhs:
                    idx = idx + 1
                    if idx == 0:
                        continue
                    global anotherIDX
                    newRule = Rule([[instantiate(stmnt,bindings)],instantiate(rule.rhs,bindings)],[[fact],[rule]])
                    newRule.name = "rule_" + str(anotherIDX)
                    anotherIDX+=1
                    fact.supports_rules.append(newRule)
                    rule.supports_rules.append(newRule)
                    kb.kb_assert(newRule)