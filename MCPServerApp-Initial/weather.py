from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """ _summary_
    Get the weather for a given city
    """
    return f"The weather in {city} is sunny"

# The transport=streamable-http is used to run the MCP server in the browser
# We can also use the transport=stdio to run the MCP server in the terminal

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
