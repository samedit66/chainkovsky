from collections import UserDict, UserList
import inspect


class chain(object):

    def __init__(self, *funcs):
        self.funcs = list(funcs)

    def __or__(self, func):
        self.funcs.append(func)
        return self

    def _params(self, func):
        p = inspect.signature(func).parameters
        return [str(p[x]) for x in p]

    def __call__(self, *args, **kwargs):
        if not self.funcs:
            return

        args = self.funcs[0](*args, **kwargs)
        for func in self.funcs[1:]:
            func_params = self._params(func)

            if not func_params:
                args = func()
            elif isinstance(args, UserDict) or isinstance(args, dict):
                if any(par.startswith("**") for par in func_params) \
                    or len(args) == len(func_params):
                    args = func(**args)
                else:
                    args = func(args)
            elif isinstance(args, UserList) or isinstance(args, tuple) or isinstance(args, list):
                if any(par.startswith("*") and not par.startswith("**") for par in func_params) \
                    or len(args) == len(func_params):
                    args = func(*args)
                else:
                    args = func(args)
            else:
                args = func(args)
        
        return args