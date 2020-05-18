class IntermediateCodeData:
    def __init__(self):
        self.quadruples = {}
        self.constant_table = None
        self.dir_func = {}
        self.player_table = {}

    def save_quads(self, quad_stack):
        while not quad_stack.empty():
            quad = quad_stack.peek_quad()
            quad_stack.pop_quad()
            quad_tuple = (quad.get_operator(), quad.left_operand(), quad.right_operand(), quad.result())
            self.quadruples[quad.id] = quad_tuple

    def save_constant_table(self, const_table):
        self.constant_table = const_table

    def save_dir_func(self, dir_func):
        for key in dir_func:
            value = dir_func[key]
            self.dir_func[key] = {}
            self.dir_func[key]['name'] = value.name
            self.dir_func[key]['temp_vars_count'] = value.temp_vars_count
            self.dir_func[key]['vars_count'] = value.vars_count
            self.dir_func[key]['func_start'] = value.func_start
            self.dir_func[key]['params_length'] = value.get_params_length()

    def save_player_table(self, player_table):
        for key in player_table:
            value = player_table[key]
            self.player_table[key] = {}
            self.player_table[key]['location'] = value.location