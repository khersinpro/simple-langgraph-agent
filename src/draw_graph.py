from config import load_environment
from pathlib import Path
from agent.react_agent import agent

def generate_graph_image():
    """Generate a PNG image of the graph and save it to the project root."""
    try:
        current_dir = Path(__file__).parent  
        root_dir = current_dir.parent  
        output_path = root_dir / "agent_graph.png"
    
        png_data = agent.get_graph().draw_mermaid_png()

        with open(output_path, "wb") as f:
            f.write(png_data)
        
        print(f"Graph saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    generate_graph_image()