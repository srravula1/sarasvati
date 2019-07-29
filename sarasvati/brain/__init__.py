
class IBrain:
    def __init__(self, storage: "Storage", components: "ComponentsManager"):
        pass

    def create_component(self, name: str) -> "Component":
        pass

    def attach_component(self, thought: "Thought", component_name: str) -> "Component":
        pass

    def save_thought(self, thought: "Thought"):
        pass

    def create_thought(self, title: str, description: str = None, key: str = None):
        pass

    def delete_thought(self, thought: "Thought"):
        pass

    def find_thoughts(self, query: dict):
        pass

    def activate_thought(self):
        pass
