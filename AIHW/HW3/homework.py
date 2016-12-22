from ply import lex
import re
from collections import OrderedDict
from copy import copy

AND = 'AND'
OR = 'OR'
NOT = 'NOT'
IMPLIES = 'IMPLIES'
NEGATED_IMPLIES = 'NEGATED_IMPLIES'
COMMA = 'COMMA'
PREDICATE = 'PREDICATE'
VARIABLE = 'VARIABLE'
CONSTANT = 'CONSTANT'
OBRACE = 'OBRACE'
EBRACE = 'EBRACE'

tokens = (
    AND,
    OR,
    NOT,
    IMPLIES,
    COMMA,
    PREDICATE,
    VARIABLE,
    CONSTANT,
    OBRACE,
    EBRACE,
    NEGATED_IMPLIES
)

t_ignore  = ' \t'
t_AND = r'\&'
t_OR = r'\|'
t_NOT = r'\~'
t_IMPLIES = r'\=\>'
t_NEGATED_IMPLIES = r'\$'
t_COMMA = r'\,'
t_OBRACE = r'\('
t_EBRACE = r'\)'

def t_PREDICATE(t):
    r'[A-Z][a-z]*\('
    t.value = t.value.replace('(', '')
    return t

def t_CONSTANT(t):
    r'[A-Z][A-Za-z]*\,|[A-Z][A-Za-z]*\)'
    t.value = re.sub(r'[\)\,]', '', t.value)
    return t

def t_VARIABLE(t):
    r'[a-z][a-z]*\,|[a-z][a-z]*\)'
    t.value = re.sub(r'[\)\,]', '', t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

VARIABLE_CONSTANT = 'VARIABLE_CONSTANT'
NEGATION = 'NEGATION'

class ReadInput(object):
    def __init__(self):
        self._query_cases = None
        self._query = list()
        self._kb_cases = None
        self._kb = list()

    @property
    def query_cases(self):
        return self._query_cases

    @property
    def query(self):
        return self._query

    @property
    def kb_cases(self):
        return self._kb_cases

    @property
    def kb(self):
        return self._kb

    def read(self):
        with open("input.txt", "r") as fp:
            lines = fp.readlines()
            self._query_cases = int(lines[0])
            #print "Query cases", self.query_cases

            query_line = 1
            for i in xrange(0, self.query_cases):
                text = str(lines[query_line+i])
                clean_text = re.sub(r'[\t\s ]', '', text)
                self._query.append(clean_text)
            #print "Query", self.query

            self._kb_cases = int(lines[self.query_cases + 1])
            #print "KB cases", self.kb_cases

            kb_line = self.query_cases + 2
            for i in xrange(0, self.kb_cases):
                text = str(lines[kb_line+i])
                clean_text = re.sub(r'[\t\s ]', '', text)
                self._kb.append(clean_text)
            #print "KB", self.kb    


#data = "((A(x) => B(x)) => ((Ghost(y) | Devil(j)) & Kill(Hell)))"
#data = "(A(x) => B(x))"
#data = "((A(x) & C(x)) => B(x))"
#data = "(F(x) | (((A(x) & C(x)) => B(x)) | E(x)))"
#data = "( A(m, Sunil) | (B(x, y) & C(a, b)) )"
#data = "((A(m, Sunil) & B(x, y)) | (E(a, b) & F(p, q)))"
#data = "((B(x, y) & C(a, b)) | A(m, Sunil))"

#data = "( ( ( (B(x, y) & C(a, b)) | A(m, Sunil)) | E(p,q)) | F(r, s))"
#data = "((B(x, y) & C(a, b)) | (A(m, Sunil) | E(p,q)))"
#data = "((G(q) & H(r)) | (((A(m) | B(n)) | C(o)) | D(p)))"
#data = "((G(q) & H(r)) | (((A(m) & B(n)) | C(o)) & D(p)))"
#data = "((~A(l,m)|B(p,q)) => (C(x,y) & ~D(p,q)))"
#data = "((~A(l,m)|B(p,q)) => (A(l,m) & ~B(p,q)))"
#data = "((~A(l,m)|B(p,q)) => (A(l,r) & ~B(p,q)))"
#data = "((D(p) & H(r)) | (((C(o) & B(n)) | C(o)) & D(p)))"

#data = "Brothers(Sunil, Gopi)"
#data = "(~(~(~(~(~(Brothers(Sunil, Gopi)))))))"
#data = "(~(~(~(~(Brothers(Sunil, Gopi))))))"

#data = "(~A(x))"
#data = "(~(A(x)))"
#data = "(~(E(x, b) & (A(x) | B(x))))"
#data = "(~ (E(x, b) & (A(x) | B(x))) | (~(R(c, e) => G(p))) )"
#data = "((~(E(x, b) => ~(A(x) | B(x)))) | (~(R(c, e) => G(p))) )"
#data = "((~(Parent(x,y) & Ancestor(y,z))) | Ancestor(x,z))"

OPERATOR_MAPPING = {
    AND: '&',
    OR: '|'
}

def tokens_print(token_list):
    result = list()
    for val in token_list:
        result.append(val.value)
    return ''.join(result)

def print_kbs(kb_lists):
    result = list()
    for kb in kb_lists:
        result.append(tokens_print(kb))
    #print result
    return result

def tokenization(data):
    token_result = list()
    for line_raw in data:
        # Give the lexer some input
        lexer.input(line_raw)
        line_token_list = list()
        # Tokenize        
        while True:
            tok = lexer.token()
            if not tok: 
                break
            line_token_list.append(tok)
        token_result.append(line_token_list)
    #print "==========================================="
    #print "Tokenization"
    #print_kbs (token_result)
    return token_result

class Node(object):
    def __init__(self, left, val, right):
        self.left = left
        self.value = val
        self.right = right

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, value):
        self._left = value

    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, value):
        self._val = value

    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value

def create_node(val):
    return Node(None, val, None)


class Stack(object):
    def __init__(self):
        self.stack = None
        self.stack_size = 0

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, val):
        self._stack = val

    def push(self, val):
        self.stack = self.node_front_insertion(val)
        self.stack_size = self.stack_size + 1
        return self.stack

    def pop(self):
        val = None
        if self.stack_size == 0:
            print "Stack is empty"
        else:
            val = self.node_front_removal()
            self.stack_size = self.stack_size - 1
        return val

    def node_front_insertion(self, val):
        if not self.stack:
            return create_node(val)
        else:
            new_node = create_node(val)
            new_node.right = self.stack
            return new_node 

    def node_front_removal(self):
        val = None
        if self.stack_size == 1:
            val = self.stack.value
            self.stack = None
        else:
            val = self.stack.value
            self.stack = self.stack.right
        return val

    def stack_top(self):
        if self.stack:
            return self.stack.value
        else:
            return None

def convert_to_postfix(line_kb):
    result = list()
    stack = Stack()
    for val in line_kb:

        tok_symbol = val.type
        
        if tok_symbol == OBRACE:
            stack.push(val)

        elif tok_symbol == AND or tok_symbol == OR\
            or tok_symbol == IMPLIES or tok_symbol == NEGATED_IMPLIES:
            stack.push(val)

        elif tok_symbol == PREDICATE or tok_symbol == VARIABLE\
            or tok_symbol == CONSTANT or tok_symbol == NOT:
            result.append(val)

        elif tok_symbol == EBRACE:
            while stack.stack and stack.stack_top().type != OBRACE:
                result.append(stack.pop())
            if stack.stack and stack.stack_top().type == OBRACE:
                stack.pop()
    while stack.stack:
        top = stack.pop()
        if (top.type != EBRACE and top.type != OBRACE):
            result.append(top)
    #print "==================================="
    #print "Postfix for input given"
    #print #tokens_print(result)
    return result


def postfix_to_infix(postfix):
    result = list()
    stack = Stack()
    for val in postfix:
        tok_symbol = val.type        
        if tok_symbol == AND or tok_symbol == OR:

            count = 2
            pop_list = list()
            pop_list.insert(0, get_cloned_token(EBRACE, ')'))
            
            while True:
                token = stack.pop()
                if token.type == EBRACE:
                    count = count - 1
                    pop_list.insert(0, token)
                    bracket_count = 1
                    while bracket_count:
                        t = stack.pop()
                        pop_list.insert(0, t)
                        if t.type == EBRACE:
                            bracket_count = bracket_count + 1
                        elif t.type == OBRACE:
                            bracket_count = bracket_count - 1
                            if not bracket_count:
                                break
                    if not count:
                        break
                    else:
                        pop_list.insert(0, val)

                elif token.type == CONSTANT or token.type == VARIABLE or token.type == NOT:
                    pop_list.insert(0, token)
                elif token.type == PREDICATE:
                    count = count - 1
                    pop_list.insert(0, token)
                    if stack.stack and stack.stack_top() and stack.stack_top().type == NOT:
                        pop_list.insert(0, stack.pop())
                    if not count:
                        break
                    else:
                        pop_list.insert(0, val)
            pop_list.insert(0, get_cloned_token(OBRACE, '('))
            for v in pop_list:
                stack.push(v)
        else:
            stack.push(val)
    while stack.stack:
        result.insert(0, stack.pop())
    
    #print "==================================="
    #print "Postfix to Infix"
    #print #tokens_print(result)
    return result

def get_cloned_token(lexmatch, lexdata, lineno=-1, lexpos=-1):
    lex_token = lex.LexToken()
    lex_token.type = lexmatch
    lex_token.value = lexdata
    lex_token.lineno = lineno
    lex_token.lexpos = lexpos
    return lex_token



def eliminate_implication(postfix):
    stack = Stack()
    result = list()
    for val in postfix:
        if not stack.stack:
            stack.push(val)
        else:
            #
            # If => is the token.
            # Then change => to | in the postfix.
            # Changing A=>B, ~AB|
            # If A=>(B|C), then ABC|=> is converted to ~ABC||
            # If (A&D)=>(B|C), then AD&BC|=> is converted to ~A~D|BC||
            # But here everything is stored in reverse order
            #
            tok_symbol = val.type
            if tok_symbol == IMPLIES:                
                tmp_result = list()
                lex_val = get_cloned_token(OR, '|')
                tmp_result.append(lex_val)
                negate_literal = False
                count = 2
                while stack.stack:
                    pop_ele = stack.pop()
                    if pop_ele.type == PREDICATE:
                        tmp_result.append(pop_ele)                     
                        if negate_literal:
                            tmp_result.append(get_cloned_token(NOT, '~'))
                        count = count - 1
                        if count == 1:
                            negate_literal = True
                        if not count:
                            break
                    elif pop_ele.type == AND or pop_ele.type == OR\
                        or pop_ele.type == NEGATED_IMPLIES or pop_ele.type == IMPLIES:
                        count = count + 1
                        if negate_literal:
                            if pop_ele.type == AND:
                                tmp_result.append(get_cloned_token(OR, '|', pop_ele.lineno, pop_ele.lexpos))
                            elif pop_ele.type == OR:
                                tmp_result.append(get_cloned_token(AND, '&', pop_ele.lineno, pop_ele.lexpos))
                            elif pop_ele.type == NEGATED_IMPLIES:
                                tmp_result.append(get_cloned_token(IMPLIES, '=>', pop_ele.lineno, pop_ele.lexpos))
                            else:
                                tmp_result.append(get_cloned_token(NEGATED_IMPLIES, '$', pop_ele.lineno, pop_ele.lexpos))
                        else:                            
                            tmp_result.append(pop_ele)
                    else:
                        tmp_result.append(pop_ele)
                tmp_result.reverse()
                for v in tmp_result:
                    stack.push(v)
                
                #print "==================================="
                #print "After applying part of implication"
                #print tmp_result
            else:
                stack.push(val)
    while stack.stack:
        result.append(stack.pop())
    result.reverse()
    #print "==================================="
    #print "Converted implication result"
    #print #tokens_print(result)
    return result

def eliminate_negated_implication(postfix):
    stack = Stack()
    result = list()
    for val in postfix:
        if not stack.stack:
            stack.push(val)
        else:
            #
            # If => is the token.
            # Then change => to $ in the postfix.
            # Changing A=>B, ~AB$
            # If A=>(B|C), then ABC|=> is converted to ~ABC||
            # If (A&D)=>(B|C), then AD&BC|=> is converted to ~A~D|BC||
            # But here everything is stored in reverse order
            #
            tok_symbol = val.type
            if tok_symbol == NEGATED_IMPLIES:                
                tmp_result = list()
                lex_val = get_cloned_token(AND, '&')
                tmp_result.append(lex_val)
                negate_literal = False
                count = 2
                while stack.stack:
                    pop_ele = stack.pop()
                    if pop_ele.type == PREDICATE:
                        tmp_result.append(pop_ele)                     
                        if negate_literal:
                            tmp_result.append(get_cloned_token(NOT, '~'))
                        count = count - 1
                        if count == 1:
                            negate_literal = True
                        if not count:
                            break
                    elif pop_ele.type == AND or pop_ele.type == OR\
                        or pop_ele.type == NEGATED_IMPLIES or pop_ele.type == IMPLIES:
                        count = count + 1
                        if negate_literal:
                            if pop_ele.type == AND:
                                tmp_result.append(get_cloned_token(OR, '|', pop_ele.lineno, pop_ele.lexpos))
                            elif pop_ele.type == OR:
                                tmp_result.append(get_cloned_token(AND, '&', pop_ele.lineno, pop_ele.lexpos))
                            elif pop_ele.type == NEGATED_IMPLIES:
                                tmp_result.append(get_cloned_token(IMPLIES, '=>', pop_ele.lineno, pop_ele.lexpos))
                            else:
                                tmp_result.append(get_cloned_token(NEGATED_IMPLIES, '$', pop_ele.lineno, pop_ele.lexpos))
                        else:                            
                            tmp_result.append(pop_ele)
                    else:
                        tmp_result.append(pop_ele)
                tmp_result.reverse()
                for v in tmp_result:
                    stack.push(v)
                
                #print "==================================="
                #print "After applying part of implication"
                #print tmp_result
            else:
                stack.push(val)
    while stack.stack:
        result.append(stack.pop())
    result.reverse()
    #print "==================================="
    #print "Converted implication result"
    #print #tokens_print(result)
    return result


def is_normalizable_and_or_operator(postfix):
    is_operator_found = False
    operator_earlier = None
    for val in postfix:
        if val.type == AND or val.type == OR:
            if is_operator_found:
                if operator_earlier == val.type:
                    continue
                else:
                    #print "==================================="
                    #print "Is AND or OR the only operator: Normalizable"
                    #print (False, None)
                    return (False, None)
            else:
                operator_earlier = val.type
                is_operator_found = True
    #print "==================================="
    #print "Is AND or OR the only operator: Normalizable"
    #print (True, operator_earlier)
    return (True, operator_earlier)




def normalize_double_negation(postfix):
    result = list()
    found_not_earlier = False
    for val in postfix:
        if val.type == NOT:
            if not found_not_earlier:
                found_not_earlier = True
            else:
                found_not_earlier = False
        else:
            # Only one not is found so adding
            if found_not_earlier:
                result.append(get_cloned_token(NOT, '~'))
                found_not_earlier = False
            result.append(val)
    #print "==================================="
    #print "Normalized normalize_double_negation"
    #print #tokens_print(result)
    return result


def normalize_and_or_operator(postfix, operator):
    #print "==================================="
    result = list()
    prev_val = None
    cur_val = None
    for val in postfix:
        if (val.type == PREDICATE or val.type == NOT) and\
            (prev_val and (prev_val.type == CONSTANT or prev_val.type == VARIABLE)):
            result.append(get_cloned_token(operator, OPERATOR_MAPPING[operator]))
            result.append(val)
            prev_val = val
        elif val.type == VARIABLE or val.type == CONSTANT\
            or val.type == PREDICATE or val.type == NOT:
            result.append(val)
            prev_val = val
    
    #print "Normalized result & and |"
    #print #tokens_print(result)
    return result

def distribute_tokens(stack, predicate_count_inbetween):
    #print "======================================="
    #print "Actual distributed tokens"
    result = list()
    if not predicate_count_inbetween:
        remove_and = stack.pop()
        #print "Logic 1 (ABC&| form)"
        rcount = 2
        part1_predicates = list()
        while rcount:
            tok = stack.pop()
            if tok.type == AND or tok.type == OR:
                part1_predicates.append(tok)
                rcount = rcount + 1
            elif tok.type == PREDICATE:
                rcount = rcount - 1
                part1_predicates.append(tok)
            elif tok.type == CONSTANT or tok.type == VARIABLE or tok.type== NOT:
                part1_predicates.append(tok)
        if stack.stack and stack.stack_top() and stack.stack_top().type == NOT:
            part1_predicates.append(stack.pop())

        lcount = 1
        part2_predicates = list()
        while lcount:
            tok = stack.pop()
            if tok.type == AND or tok.type == OR:
                part2_predicates.append(tok)
                lcount = lcount + 1
            elif tok.type == PREDICATE:
                lcount = lcount - 1
                part2_predicates.append(tok)
            elif tok.type == CONSTANT or tok.type == VARIABLE or tok.type== NOT:
                part2_predicates.append(tok)
        if stack.stack and stack.stack_top() and stack.stack_top().type == NOT:
            part2_predicates.append(stack.pop())

        #print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        #print part1_predicates
        #print part2_predicates

        wait_till_predicate = list()
        for val in part1_predicates:
            if val.type == AND or val.type == OR or val.type == NOT:
                result.insert(0, val)
            elif val.type == CONSTANT or val.type == VARIABLE:
                wait_till_predicate.append(val)
            elif val.type == PREDICATE:
                result.insert(0, get_cloned_token(OR, '|'))
                for j in part2_predicates:
                    result.insert(0, j)
                for i in wait_till_predicate:
                    result.insert(0, i)
                result.insert(0, val)                
                wait_till_predicate = list()
        
        result.append(get_cloned_token(AND, '&'))
        #tokens_print(result)
        return result
    else:
        #print "Logic 2 (BC&A| form)"
        found_and = False
        part1_predicates = list()
        while not found_and:
            tok = stack.pop()
            if tok.type == AND:
                found_and = True
            elif tok.type == PREDICATE or tok.type == CONSTANT\
                or tok.type == VARIABLE or tok.type == NOT:
                part1_predicates.append(tok)

        lcount = 2
        part2_predicates = list()
        while lcount:
            tok = stack.pop()
            if tok.type == AND or tok.type == OR:
                part2_predicates.append(tok)
                lcount = lcount + 1
            elif tok.type == PREDICATE:
                lcount = lcount - 1
                part2_predicates.append(tok)
            elif tok.type == CONSTANT or tok.type == VARIABLE or tok.type == NOT:
                part2_predicates.append(tok)
        
        if stack.stack and stack.stack_top().type == NOT:
            part2_predicates.append(stack.pop())

        #print "111111111111111111111111111111111"
        #print part1_predicates
        #print part2_predicates

        wait_till_predicate = list()
        for val in part2_predicates:
            if val.type == AND or val.type == OR or val.type == NOT:
                result.insert(0, val)
            elif val.type == CONSTANT or val.type == VARIABLE:
                wait_till_predicate.append(val)
            elif val.type == PREDICATE:
                result.insert(0, get_cloned_token(OR, '|'))
                for j in part1_predicates:
                    result.insert(0, j)
                for i in wait_till_predicate:
                    result.insert(0, i)
                result.insert(0, val)                
                wait_till_predicate = list()
        
        result.append(get_cloned_token(AND, '&'))
        
        #tokens_print(result)
        return result


def apply_distributive_property(postfix):
    
    is_and_found = False
    predicate_count_inbetween = 0
    stack = Stack()
    result = list()
    
    is_distribution_done = False
    for idx, val in enumerate(postfix):
        if is_distribution_done:
            stack.push(val)
            continue
        if val.type == AND:
            is_and_found = True
            predicate_count_inbetween = 0
            stack.push(val)
            continue
        elif val.type == OR and is_and_found:
            or_index = idx
            if predicate_count_inbetween == 1:
                stack.push(val)
            result = distribute_tokens(stack, predicate_count_inbetween)
            for dist in result:
                stack.push(dist)
            is_distribution_done = True
            continue
        elif val.type == PREDICATE and is_and_found:
            predicate_count_inbetween = predicate_count_inbetween + 1
            stack.push(val)
            if predicate_count_inbetween > 1:
                predicate_count_inbetween = 0
                is_and_found = False
        else:
            stack.push(val)


    final_result = list()
    while stack.stack:
        token = stack.pop()
        final_result.insert(0, token)
    #print "======================================="
    #print "Find the possible distribution & giving final distributed result"
    #tokens_print(final_result)
    return final_result

def change_all_consecutive_ors(postfix, mapping, count):
    #print "===================================="
    prev_dict_len = 0
    pre_len_mapping = 0
    final_result = list()
    check = 0
    while True:
        stack = Stack()
        for val in postfix:
            if val.type == OR:
                predicate_count = 2
                or_list = list()
                found_consecutive_or = False
                while stack.stack:
                    tok = stack.pop()
                    if tok.type == PREDICATE:
                        or_list.insert(0, tok)
                        predicate_count = predicate_count - 1
                        if not predicate_count:
                            top_stack = stack.stack_top()
                            if top_stack and top_stack.type == NOT:
                                or_list.insert(0, stack.pop())
                            found_consecutive_or = True
                            break
                    elif tok.type == AND or tok.type == OR:
                        stack.push(tok)
                        for val_tok in or_list:
                            stack.push(val_tok)
                        stack.push(val)
                        break
                    else:
                        or_list.insert(0, tok)
                if found_consecutive_or:
                    mapping[str(count)] = or_list                    
                    stack.push(get_cloned_token(PREDICATE, str(count)))
                    count = count + 1
            else:
                stack.push(val)

        final_result = list()
        while stack.stack:
            token = stack.pop()
            final_result.insert(0, token)
        postfix = final_result

        if pre_len_mapping != len(mapping):            
            pre_len_mapping = len(mapping)
        else:
            break
    #print "change_all_consecutive_ors"
    #print #tokens_print(final_result), mapping
    return (final_result, mapping, count)





def execute_distributive(postfix):
    prev_postfix = postfix
    mapping = OrderedDict()
    count = 1
    while True:
        (mapped_postfix, mapping, count) = change_all_consecutive_ors(prev_postfix, mapping, count)
        dist_postfix = apply_distributive_property(mapped_postfix)
        if dist_postfix == prev_postfix:
            break
        else:
            prev_postfix = dist_postfix
    return (prev_postfix, mapping)

def remap_substitued_ors(dist_postfix, mapping):
    while mapping:
        new_postfix = list()
        lastkey = mapping.keys()[-1]
        for tok in dist_postfix:
            if tok.value == lastkey and tok.type == PREDICATE:
                new_postfix.extend(mapping[lastkey])
                new_postfix.append(get_cloned_token(OR, '|'))
            else:
                new_postfix.append(tok)
        del mapping[lastkey]
        dist_postfix = new_postfix
    #print "Re substituing result"
    #print #tokens_print(dist_postfix)
    return dist_postfix

def split_on_conjunction(infix):
    #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    #print "Split on conjunction"
    kb_lists = list()
    start_idx = 0
    for idx, tok in enumerate(infix):
        if tok.type == AND:
            kb_lists.append(infix[start_idx:idx])
            start_idx = idx + 1
    kb_lists.append(infix[start_idx:])
    #print_kbs (kb_lists)
    return kb_lists

#a = [LexToken(PREDICATE,'A',1,3), LexToken(VARIABLE,'l',1,5),\
#LexToken(VARIABLE,'m',1,7), LexToken(OR,'|',-1,-1), LexToken(PREDICATE,'A',1,20), LexToken(VARIABLE,'l',1,22)]

def remove_duplicate_from_query(kb):
    #print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    kb_len = len(kb)
    ref_list = list()
    result = list()
    #print "Kb len", kb_len
    for i in xrange(0, kb_len):
        ref_list.append(True)
    for i in xrange(0, kb_len - 1):
        #print ref_list
        if not ref_list[i]:
            continue
        result.append(kb[i])
        if not (kb[i].type != PREDICATE or kb[i].type != NOT):
            continue
        for j in xrange(i+1, kb_len):
            if not (kb[j].type == kb[i].type and kb[i].value == kb[j].value\
                    and (kb[j].type == PREDICATE or kb[j].type == NOT)):
                continue
            #print "i, j, sptr"
            #print i, j, kb[i], kb[j]
            const_var_encountered = False
            for k in xrange(1, kb_len - j):
                if (kb[i+k].type == PREDICATE or kb[i+k].type == NOT) and const_var_encountered:
                    #print "Found not or predicate, i, j, k, kb[i+k].value, kb[j+k].value"
                    #print i, j, k, kb[i+k].value, kb[j+k].value
                    m = j
                    while m <= j+k:
                        ref_list[m] = False
                        m = m + 1
                elif kb[i+k].value == kb[j+k].value:
                    #print "Equals i, j, k, kb[i+k].value, kb[j+k].value"
                    #print i, j, k, kb[i+k].value, kb[j+k].value
                    if (j+k) == kb_len - 1:
                        #print "Inside last element match"
                        m = j
                        while m <= kb_len - 1:
                            ref_list[m] = False
                            m = m + 1
                    if kb[i+k].type == CONSTANT or kb[i+k].type == VARIABLE:
                        const_var_encountered =  True
                else:
                    #print "Breaking, i, j, k, kb[i+k].value, kb[j+k].value"
                    #print i, j, k, kb[i+k].value, kb[j+k].value
                    break
    if ref_list[-1]:
        result.append(kb[-1])
    #print result
    return result

def normalize_kbs(kb_list):
    final_result = list()
    for postfix in kb_list:
        (is_normalizable, operator) = is_normalizable_and_or_operator(postfix)
        if is_normalizable:
            normalized_kb = normalize_and_or_operator(postfix, operator)
            kb = remove_duplicate_from_query(normalized_kb)
            normalized_kb = normalize_and_or_operator(kb, operator)
            final_result.append(normalized_kb)
        else:
            #print postfix
            final_result.append(postfix)
            raise Exception("Check this.... This is still in postfix expression")
    #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    #print "Normalized kbs"
    #print_kbs (final_result)
    return final_result


def convert_to_cnf(knowledge_base):
    final_result = list()
    for data in knowledge_base:
        postfix = convert_to_postfix(data)
        imply_eliminate = eliminate_implication(postfix)
        imply_eliminate = normalize_double_negation(imply_eliminate)
        imply_eliminate = eliminate_negated_implication(imply_eliminate)
        imply_eliminate = normalize_double_negation(imply_eliminate)
        (is_normalizable, operator) = is_normalizable_and_or_operator(imply_eliminate)
        infix = None
        if is_normalizable:
            infix = normalize_and_or_operator(imply_eliminate, operator)
        else:
            (postfix, mapping) = execute_distributive(imply_eliminate)
            remapped_list = remap_substitued_ors(postfix, mapping)
            infix = postfix_to_infix(remapped_list)
        kbs = split_on_conjunction(infix)
        final_result.extend(normalize_kbs(kbs))
    return final_result

NON_NEGATION_PREDICATE = 'NON_NEGATION_PREDICATE'
NEGATION_PREDICATE = 'NEGATION_PREDICATE'
CONSTANT_PREDICATE = 'CONSTANT_PREDICATE'

def create_predicate_lookup(kbs, predicate_map):
    #print "=========================================="
    for idx, kb in enumerate(kbs):
        kb_split_list = list()
        start_idx = 0
        for i, tok in enumerate(kb):
            if tok.type == AND or tok.type == OR:
                kb_split_list.append(kb[start_idx:i])
                start_idx = i + 1
        kb_split_list.append(kb[start_idx:])
        #print kb_split_list
        
        for kb_split_list in kb_split_list:
            is_negation_predicate = False
            #print kb_split_list
            if kb_split_list and kb_split_list[0] and kb_split_list[0].type == NOT:
                is_negation_predicate = True
            for val in kb_split_list:
                if val.type == PREDICATE:
                    if is_negation_predicate:
                        predicate_map[NEGATION_PREDICATE].setdefault(val.value, []).\
                            append([val.value, kb_split_list, kb, idx])
                    else:
                        predicate_map[NON_NEGATION_PREDICATE].setdefault(val.value, []).\
                            append([val.value, kb_split_list, kb, idx])
                elif val.type == CONSTANT:
                    predicate_map[CONSTANT_PREDICATE].setdefault(val.value, []).\
                            append([val.value, kb_split_list, kb, idx])
    #print "Predicate map"
    #print predicate_map
    return predicate_map

def check_single_predicate_negation(tokens):
    is_negation_predicate = False
    if tokens and tokens[0] and tokens[0].type == NOT:
        is_negation_predicate = True
    return is_negation_predicate

def kb_split_on_or(kb):
    #print "================================================"
    #print "kb_split_on_or"
    #print kb
    kb_split_list = list()
    start_idx = 0
    for i, tok in enumerate(kb):
        if tok.type == OR:
            kb_split_list.append(kb[start_idx:i])
            start_idx = i + 1
    kb_split_list.append(kb[start_idx:])
    return kb_split_list

def remove_complete_token_using_predicate(remove_predicate, tokens):
    #print "---------------------------------------------------"
    #print "remove_complete_token_using_predicate"
    #print remove_predicate
    #print tokens
    token_split = kb_split_on_or(tokens)
    result = list()
    for tok in token_split:
        if len(remove_predicate) != len(tok):
            result.extend(tok)
            result.append(get_cloned_token(OR, '|'))
            continue
        for i in xrange(0, len(remove_predicate)):
            if remove_predicate[i].type == tok[i].type and remove_predicate[i].value == tok[i].value:
                continue
            result.extend(tok)
            result.append(get_cloned_token(OR, '|'))
            break
    result = result[:-1]
            
    #print "========================================"
    #print "Removing unification predicate"
    #print result
    return result
    

def negate_all_tokens(tokens_list):
    final_result = list()
    for tokens in tokens_list:
        result = list()
        for tok in tokens:
            if tok.type == PREDICATE:
                result.append(get_cloned_token(NOT, '~'))
                result.append(tok)
            elif tok.type == AND:
                result.append(get_cloned_token(OR, '|'))
            elif tok.type == OR:
                result.append(get_cloned_token(AND, '&'))
            else:
                result.append(tok)
        final_result.append(result)
    return final_result

def get_predicate_variable_names(tokens):
    kb_split_list = kb_split_on_or(tokens)
    token_info_list = dict()
    
    for kb_split_list in kb_split_list:
        is_negation_predicate = False
        
        if kb_split_list and kb_split_list[0] and kb_split_list[0].type == NOT:
            is_negation_predicate = True
        
        constant_list = list()
        var_constant_list = list()
        for val in kb_split_list:
            if val.type == PREDICATE:
                token_info_list[PREDICATE] = val
            if val.type == CONSTANT or val.type == VARIABLE:
                var_constant_list.append(val)
            if val.type == CONSTANT:
                constant_list.append(val) 
        token_info_list[VARIABLE_CONSTANT] = var_constant_list
        token_info_list[NEGATION] = is_negation_predicate
        token_info_list[CONSTANT] = constant_list
    return token_info_list


def add_single_predicate_to_kb(predicate_info, predicate_map, kb_len):
    #print predicate_info
    var_constant = predicate_info[VARIABLE_CONSTANT]
    constant = predicate_info[CONSTANT]
    predicate = predicate_info[PREDICATE]
    predicate_list = list()
    predicate_list.append(predicate)  
    predicate_list.extend(var_constant)

    if predicate_info[NEGATION]:
        predicate_list.insert(0, get_cloned_token(NOT, '~'))
        predicate_map[NEGATION_PREDICATE].setdefault(predicate.value, []).\
                            append([predicate.value, predicate_list, predicate_list, kb_len])
    else:
        predicate_map[NON_NEGATION_PREDICATE].setdefault(predicate.value, []).\
                            append([predicate.value, predicate_list, predicate_list, kb_len])

    for const in constant:
        predicate_map[CONSTANT_PREDICATE].setdefault(const.value, []).\
                                append([const.value, predicate_list, predicate_list, kb_len])
    return predicate_map

    

def add_query_token_to_kb(query_token, predicate_map, kbs):
    query_token = tokenization(query_token)
    #print query_token
    query_negate = negate_all_tokens(query_token)
    #print query_negate
    
    
    query_token_cnf = convert_to_cnf(query_negate)
    #print "Converting to cnf"
    #print query_token_cnf
    kbs.append(query_token_cnf[0])

    predicate_info = get_predicate_variable_names(query_token_cnf[0])
    new_predicate_map = add_single_predicate_to_kb(predicate_info, predicate_map, len(kbs))
    #print "======================================================"
    #print "new_predicate_map"
    #print new_predicate_map
    return (kbs, new_predicate_map)


def normalize_single_variable_kb(kb1):
    #print token1, token2, kb1, kb2
    count = 0
    replace_var_dict1 = dict()
    for tok in kb1:
        if tok.type == VARIABLE:
            if tok.value not in replace_var_dict1:
                count = count + 1
                replace_var_dict1[tok.value] = str(count)                
                tok.value = str(count)
            else:
                tok.value = replace_var_dict1[tok.value]
    return kb1


def normalize_variables(token1, token2, kb1, kb2):
    #print token1, token2, kb1, kb2
    count = 0
    replace_var_dict1 = dict()
    for tok in kb1:
        if tok.type == VARIABLE:
            if tok.value not in replace_var_dict1:
                count = count + 1
                replace_var_dict1[tok.value] = str(count)                
                tok.value = str(count)
            else:
                tok.value = replace_var_dict1[tok.value]

    # Because the token1 & Kb1 are reference variables.
    # Modification of one changes the other
    """
    print replace_var_dict1
    print token1, kb1
    for tok in token1:
        if tok.type == VARIABLE:
            print tok.value
            tok.value = replace_var_dict1[tok.value]
    """

    replace_var_dict2 = dict()
    for tok in kb2:
        if tok.type == VARIABLE:
            if tok.value not in replace_var_dict2:
                count = count + 1
                replace_var_dict2[tok.value] = str(count)                
                tok.value = str(count)
            else:
                tok.value = replace_var_dict2[tok.value]
    # Because the token1 & Kb1 are reference variables.
    # Modification of one changes the other
    """
    for tok in token2:
        if tok.type == VARIABLE:
            tok.value = replace_var_dict2[tok.value]
    """
    return (token1, token2, kb1, kb2)

def split_sort_on_or(str_list):
    text_list = str_list.split('|')
    text_list.sort()
    return '|'.join(text_list)





def resolution(kbs, predicate_map):
    #print "----------------------------------------"
    #print print_kbs(kbs)
    new_kbs = list()
    is_proved = False
    kb_str_dict = dict()
    for x in  print_kbs(kbs):
        x = split_sort_on_or(x)
        kb_str_dict[x] = x
    old_kb_len = 0

    while (not (is_proved or old_kb_len == len(kb_str_dict))) and len(kb_str_dict) < 1001:
        #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        #print print_kbs(new_kbs)
        #print is_proved, old_kb_len, len(kb_str_dict)

        old_kb_len = len(kb_str_dict)
        new_kbs = list()
        for neg_key, neg_value in predicate_map['NEGATION_PREDICATE'].iteritems():
            if neg_key not in predicate_map['NON_NEGATION_PREDICATE']:
                continue
            
            non_negation_list = predicate_map['NON_NEGATION_PREDICATE'][neg_key]

            #print "---------- &&&&&&&&&&&&&&"
            #for x in non_negation_list:
            #    print tokens_print(x[2])
            #
            #for x in neg_value:
            #    print tokens_print(x[2])
            #print "----------"


            for neg_info_list in neg_value:
                neg_tokens = neg_info_list[1]
                neg_kb = neg_info_list[2]
                for non_neg_info_list in non_negation_list:
                    non_neg_token = non_neg_info_list[1]
                    non_neg_kb = non_neg_info_list[2]
                    if (len(neg_tokens) - 1) != len(non_neg_token):
                        continue
                    #print tokens_print(non_neg_kb), tokens_print(neg_kb)

                    (neg_tokens, non_neg_token, neg_kb, non_neg_kb) = \
                        normalize_variables(neg_tokens, non_neg_token, neg_kb, non_neg_kb)

                    #print "********************"
                    #print tokens_print(neg_tokens)
                    #print tokens_print(non_neg_token)
                    #print tokens_print(neg_kb)
                    #print tokens_print(non_neg_kb)

                    unification_dict = dict()
                    is_unification = True
                    for k in xrange(1, len(non_neg_token)):
                        if neg_tokens[k+1].type == VARIABLE and non_neg_token[k].type == CONSTANT:
                            unification_dict[neg_tokens[k+1].value] = (non_neg_token[k].value, True)
                        elif neg_tokens[k+1].type == CONSTANT and non_neg_token[k].type == VARIABLE:
                            unification_dict[non_neg_token[k].value] = (neg_tokens[k+1].value, True)
                        elif neg_tokens[k+1].type == CONSTANT and non_neg_token[k].type == CONSTANT\
                            and neg_tokens[k+1].value == non_neg_token[k].value:
                            continue
                        elif neg_tokens[k+1].type == VARIABLE and non_neg_token[k].type == VARIABLE:
                            unification_dict[neg_tokens[k+1].value] = (neg_tokens[k+1].value, False)
                            unification_dict[non_neg_token[k].value] = (neg_tokens[k+1].value, False)
                        else:
                            is_unification = False
                            break

                    if is_unification:
                        #print "+++++++++++++++++++++="
                        #print tokens_print(neg_kb)
                        #print tokens_print(non_neg_kb)
                        #print '---'
                        unified = remove_complete_token_using_predicate(neg_tokens, neg_kb)
                        non_neg_unified = remove_complete_token_using_predicate(non_neg_token, non_neg_kb)
                        if unified and non_neg_unified:
                            unified.append(get_cloned_token(OR, '|'))
                        
                        unified.extend(non_neg_unified)
                        unified_clone_list = list()
                        for uni_token in unified:
                            unified_clone_list.append(get_cloned_token(uni_token.type, uni_token.value))


                        if not unified_clone_list:
                            #print "^^^^^^^^^^^^^^^^^^^^^^^^ &&&&&&&&&&&&&&&&&& *********"
                            #print tokens_print(unified) 
                            #print tokens_print(neg_kb)
                            #print tokens_print(non_neg_kb)
                            #print '######################################################'
                            is_proved = True
                            break

                        #print "-----------------"
                        #print unification_dict
                        #print unified_clone_list
                        for t in unified_clone_list:
                            if t.type == VARIABLE:
                                if t.value in unification_dict:
                                    dict_val = unification_dict.get(t.value)
                                    if dict_val[1]:
                                        t.type = CONSTANT
                                    t.value = dict_val[0]
                        
                        unified_clone_list = normalize_single_variable_kb(unified_clone_list)

                        #print "unified"
                        #print unified
                        unified_string_list = tokens_print(unified_clone_list)
                        unified_string_list = split_sort_on_or(unified_string_list)
                        #print unified_string_list
                        if unified_string_list not in kb_str_dict:
                            kb_str_dict[unified_string_list] = unified_string_list
                            new_kbs.append(unified_clone_list)
                            #print tokens_print(unified)
        #print print_kbs(new_kbs)
        #print kb_str_dict.keys()
        
        #print "======================================"
        predicate_map = create_predicate_lookup(new_kbs, predicate_map)
        #print predicate_map
    if is_proved:
        return "TRUE"
    else:
        return "FALSE"

def write_to_output(result_list):
    with open("output.txt", "w") as fp:
        for result in result_list:
            fp.write(str(result) + '\n')


def move_negation_inside_bracket(kb_token):
    #print "========================================================="
    #print "move_negation_inside_bracket"
    all_kb_result = list()
    for kb in kb_token:
        kb_list = list()
        prev_kb = []
        #print tokens_print (kb_list)
        while tokens_print(kb) != tokens_print(prev_kb):
            #print "========================================================="
            #print tokens_print (kb)
            prev_kb = kb
            kb_list = list()   
            negation_loop = False
            prev_token_type = None
            open_bracket_count = 0
            for idx, token in enumerate(kb):
                #print "-------------------------------------------"
                #print "token.value, token.type, prev_token_type"
                #print token.value, token.type, prev_token_type
                #print "prev_token_type , open_bracket_count, token.type"
                #print prev_token_type , open_bracket_count, token.type
                if prev_token_type == NOT and (not open_bracket_count) and token.type == OBRACE:
                    #print "Assigment Not openbracket type"
                    negation_loop = True
                    open_bracket_count = 1
                    kb_list.append(token)
                elif negation_loop and open_bracket_count == 1:
                    #print "negation_loop and bracket count"
                    if token.type == PREDICATE:
                        kb_list.append(get_cloned_token(NOT, '~'))
                        kb_list.append(token)
                    elif token.type == AND:
                        kb_list.append(get_cloned_token(OR, '|'))
                    elif token.type == OR:
                        kb_list.append(get_cloned_token(AND, '&'))
                    elif token.type == OBRACE:
                        kb_list.append(get_cloned_token(NOT, '~'))
                        kb_list.append(token)
                        open_bracket_count = open_bracket_count + 1
                    elif token.type == EBRACE:
                        kb_list.append(token)
                        open_bracket_count = open_bracket_count - 1
                        if not open_bracket_count:
                            negation_loop = False
                            open_bracket_count = 0
                    elif token.type == NOT:
                        prev_token_type = token.type
                        kb_list.append(token)
                        #print tokens_print(kb_list)
                        continue
                    elif token.type == NEGATED_IMPLIES:
                        kb_list.append(get_cloned_token(IMPLIES, '=>'))
                    elif token.type == IMPLIES:
                        kb_list.append(get_cloned_token(NEGATED_IMPLIES, '$'))
                    else:
                        kb_list.append(token)
                else:
                    #print "Nothing doing just appendinb"
                    if token.type == NOT:
                        if kb[idx+1].type == OBRACE and not negation_loop:
                            prev_token_type = token.type
                            #print tokens_print(kb_list)
                            continue
                    kb_list.append(token)
                #print tokens_print(kb_list)
                prev_token_type = token.type
            kb = kb_list
        all_kb_result.append(kb_list)
    #print print_kbs(all_kb_result)
    return all_kb_result

def main():
    #print "##########################################################"
    read_input = ReadInput()
    read_input.read()
    kb_token = tokenization(read_input.kb)
    knowledge_base = move_negation_inside_bracket(kb_token)
    kbs = convert_to_cnf(knowledge_base)

    
    #print "==================== KBS ======================="
    #print_kbs (kbs)
    #print "==================== PREDICATE MAP ======================="
    

    #print predicate_map
    resolution_result = list()
    query_tokens = read_input.query
    for query_token in query_tokens:
        query_token_list = list()
        query_token_list.append(query_token)
        #print query_token_list
    

        kb_new = list()
        for kb in kbs:
            normalized_kb = normalize_single_variable_kb(kb)
            kb_sub_list = list()
            for tok in normalized_kb:
                kb_sub_list.append(get_cloned_token(tok.type, tok.value))
            kb_new.append(kb_sub_list)

        predicate_map_schema = {
            NON_NEGATION_PREDICATE : dict(),
            NEGATION_PREDICATE : dict(),
            CONSTANT_PREDICATE : dict()
        }

        predicate_map = create_predicate_lookup(kb_new, predicate_map_schema)
        #print predicate_map
        
        #query_token_list = ['G(Tom)']
        (new_kbs, new_predicate_map) = add_query_token_to_kb(query_token_list,\
            predicate_map, kb_new)
        resolution_result.append(resolution(new_kbs, new_predicate_map))
    
    write_to_output(resolution_result)
    #print query_tokens
    #print resolution_result

   

if __name__ == "__main__":
    main()
    