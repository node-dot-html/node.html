import html_model

class HtmlHandler:

    def __init__(self):
        self.tag_stack = []
        self.handle_tree = None
        self.start_token_router = {
            'p' : self.handle_start_p,
            'article' : self.handle_start_article,
            'var' : self.handle_start_var,
            'input' : self.handle_start_input,
        }

        self.end_token_router = {
            'p': self.handle_end_p,
            'article': self.handle_end_article,
            'var': self.handle_end_var,
            'input': self.handle_end_input,
        }



    def handle_start_p(self,tag,attrs):
        p_model = html_model.P(tag)
        if len(self.tag_stack) > 0:
            self.tag_stack[-1].add_child(p_model)
        if self.handle_tree is None:
            self.handle_tree = p_model
        self.tag_stack.append(p_model)

    def handle_end_p(self):
        p_model = self.tag_stack.pop()
        p_model.run()

    def handle_start_article(self, tag, attrs):
        article_model = html_model.Article(tag)
        if len(self.tag_stack) > 0:
            self.tag_stack[-1].add_child(article_model)
        self.tag_stack.append(article_model)

    def handle_end_article(self):
        article_model = self.tag_stack.pop()
        article_model.run()

    def handle_start_var(self, tag, attrs):
        var_model = html_model.Var(tag)
        if len(self.tag_stack) > 0:
            self.tag_stack[-1].add_child(var_model)
        self.tag_stack.append(var_model)

    def handle_end_var(self):
        self.tag_stack.pop()

    def handle_start_input(self, tag, attrs):
        input_model = html_model.Input(tag,attrs)
        self.tag_stack.append(input_model)

    def handle_end_input(self):
        input_model = self.tag_stack.pop()
        input_model.run()

    def handle_data(self,data):
        data = data.strip()
        if data == '':
            return
        if len(self.tag_stack) == 0:
            return
        model = self.tag_stack[-1]
        if type(model) is html_model.Var:
            model.setName(data)
        if type(model) is html_model.Article:
            model.add_child(data)