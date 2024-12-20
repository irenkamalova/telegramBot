import os

class CommandsScanner:
    def __init__(self):
        self.commands_path = os.path.join(os.path.dirname(__file__), 'commands')

    def get_command_instances(self):
        instances = []
        for filename in os.listdir(self.commands_path):
            if filename.endswith('.py') and filename != '__init__.py':
                # Import the command class dynamically and instantiate it
                module_name = filename[:-3]  # Remove the '.py' extension
                module = __import__(f'commands.{module_name}', fromlist=[module_name])
                command_class = getattr(module, module_name.capitalize() + 'Command')
                instances.append(command_class())
        return instances
