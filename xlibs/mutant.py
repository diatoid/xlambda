'''Mutant Classes'''
from typing import List

from xlibs import async_lambda
from xlibs.utils import get_function_name
from xlibs.professor import constants


class Mutant():
    '''Boilerplate for a Mutant class representing a Lambda worker'''

    def __init__(self, *args, **kwargs):
        self._name = None
        self._function_name = None

    @property
    def function_name(self) -> str:
        if not self._function_name:
            self._function_name = get_function_name(function=self._name)

        return self._function_name

    def execute(self, requests: List) -> List:
        '''Invoke a Mutant Lambda'''
        return async_lambda.invoke_all(
            requests=requests,
            region=constants.REGION,
        )


class Wolverine(Mutant):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = 'wolverine'

    def get_metrics(self, functions: List) -> List:
        '''Get metrics from CloudWatch'''
        requests = [
            {
                'function_name': self.function_name,
                'payload': function,
            }
            for function in functions
        ]

        response = self.execute(requests=requests)

        return [
            payload['data']
            for payload in response
            if payload['status'] == 200
        ]


class Jean(Mutant):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = 'jean'

    def forecast(self, functions_metrics: List, timeframe: int) -> List:
        '''Forecast future demand for a list of Lambda functions'''
        requests = [
            {
                'function_name': self.function_name,
                'payload': {**function, **{'timeframe': timeframe}},
            }
            for function in functions_metrics
        ]

        response = self.execute(requests=requests)

        return [
            payload['data']
            for payload in response
            if payload['status'] == 200
        ]


class Cyclops(Mutant):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = 'cyclops'

    def burn(self, functions_demand: List) -> List:
        '''Warm up a list of Lambdas'''
        requests = [
            {
                'function_name': self.function_name,
                'payload': function,
            }
            for function in functions_demand
        ]

        response = self.execute(requests=requests)

        return [
            payload['data']
            for payload in response
            if payload['status'] == 200
        ]
