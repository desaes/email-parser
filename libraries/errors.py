class EmptyVariableError(Exception):
    def __init__(self, variable_name) -> None:
        """
        This error can be used to raise a exception when a empty variable is used
        Args:
            message: Error message to be displayed.
            variable: Name of the variable to be displayed in the error message.
        Returns:
            Nothing.
        Raises:
            Nothing.
        """
        super().__init__(f'Error code 1: The variable {variable_name} is empty')

class InvalidValueError(Exception):
    def __init__(self, message) -> None:
        """
        This error can be used to raise an exception when the value of a variable
        is different of the expected value
        Args:
            message: Error message to be displayed.
            variable: Name of the variable to be displayed in the error message.
        Returns:
            Nothing.
        Raises:
            Nothing.
        """
        super().__init__(f'Error code 2: {message}')

"""
raise RuntimeErrorWithCode('Example error message', 500)
err = EmptyVariableError('An error happened.', 'variable')
print(err.__doc__) # display the docstring
"""
