import datetime

class Parameter(object):
    def __init__(self, name, flags=(), choices=None, default=None, description="?", ask=True, **kwargs):
        super(Parameter, self).__init__()
        self.name = name
        self.choices = choices
        self.default = default
        self.description = description
        self.flags = flags
        self.ask = ask
        self.kwargs = kwargs
    def add_to_parser(self, parser):
        parser.add_argument(dest=self.name, choices=self.choices, default=None, help=self.description, *self.flags, **self.kwargs)

class Parameters(object):
    def __init__(self, parameters):
        super(Parameters, self).__init__()
        self.parameters = parameters
    def populate_parser(self, parser):
        for parameter in self.parameters:
            parameter.add_to_parser(parser)
    def build_context(self, args, interactive=False):
        returned = {"supported_versions": ["2.6", "2.7", "3.3"]}
        for parameter in self.parameters:
            value = getattr(args, parameter.name)
            if value is None:
                if interactive and parameter.ask:
                    question = parameter.description
                    if parameter.default is not None:
                        question += "(default: {})".format(parameter.default)
                    value = raw_input("{}? ".format(question)).strip()
                if not value:
                    value = parameter.default
            returned[parameter.name] = value
        returned["year"] = datetime.date.today().year
        return returned

LICENSES = {
    "Proprietary",
    "BSD3",
}

parameters = Parameters([
    Parameter("license_name", ["--license"], default="Proprietary", choices=list(LICENSES.copy()),
              description="License type ({})".format("/".join(sorted(LICENSES)))),
    Parameter("name", ["--name"], description="Package name"),
    Parameter("description", ["--description"], description="Package description"),
    Parameter("author_fullname", ["--author"], description="Author name"),
    Parameter("author_email", ["--email"], description="Author email"),
    Parameter("url", ["--url"], description="Project URL"),
    Parameter("github_username", ["--github-user"], description="Github username", default=None),
])
