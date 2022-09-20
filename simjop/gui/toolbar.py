class ToolBarLogic:
    def __init__(self, toolbar, toggle_group):
        self._toolbar = toolbar
        self._toggle_group = toggle_group

    def _get_tools(self):
        tools = {}
        for i in range(self._toolbar.GetToolsCount()):
            tool = self._toolbar.GetToolByPos(i)
            tools[tool.Label] = {
                "id": tool.Id,
                "state": self._toolbar.GetToolState(tool.Id),
                "enabled": self._toolbar.GetToolEnabled(tool.Id),
            }
        return tools

    def on_button(self, button):
        tools = self._get_tools()
        if (
            tools[button]["enabled"]
            and tools[button]["state"]
            and button in self._toggle_group
        ):
            for tool in self._toggle_group:
                if tool != button and tools[tool]["enabled"] and tools[tool]["state"]:
                    self._toolbar.ToggleTool(tools[tool]["id"], False)
        return tools[button]["enabled"] and tools[button]["state"]
