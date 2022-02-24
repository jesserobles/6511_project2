

class FileParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.parsed_payload = self.parse_file()
    
    def parse_file(self) -> dict:
        """Method to parse a graph coloring problem input file"""
        # Use set to remove duplicate edges
        edges = []
        csp_payload = {}
        with open(self.filepath, "r") as file:
            for line in file:
                if not line.strip() or line.strip().startswith('#'):
                    # Skip empty lines and comments
                    continue
                if line.lower().strip().startswith('colors'):
                    # Color line
                    csp_payload["colors"] = int(line.split('=')[-1].strip())
                else:
                    # Edge line
                    edges.append(tuple(sorted(int(element.strip()) for element in line.strip().split(','))))
        csp_payload["edges"] = edges
        return csp_payload

if __name__ == "__main__":
    import os
    filepath = os.path.join("assets", "gc_1378296846561000.txt")
    fp = FileParser(filepath)
    print(fp.parse_file())