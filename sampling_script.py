import random
import pandas as pd
from typing import List, Union
import sys
import argparse

class RDProjectRandomizer:
    """
    A tool to randomly select R&D projects for tax credit documentation.
    Supports both Excel files and Python lists as input.
    """
    
    def __init__(self, seed=None):
        """Initialize with optional random seed for reproducible results."""
        if seed:
            random.seed(seed)
    
    def load_projects_from_excel(self, file_path: str, project_column: str = None) -> List[str]:
        """
        Load projects from an Excel file.
        
        Args:
            file_path: Path to Excel file
            project_column: Name of column containing project names (if None, uses first column)
        
        Returns:
            List of project names
        """
        try:
            df = pd.read_excel(file_path)
            
            if project_column:
                if project_column not in df.columns:
                    raise ValueError(f"Column '{project_column}' not found in Excel file")
                projects = df[project_column].dropna().tolist()
            else:
                # Use first column if no column specified
                projects = df.iloc[:, 0].dropna().tolist()
            
            # Convert to strings and remove empty entries
            projects = [str(project).strip() for project in projects if str(project).strip()]
            
            print(f"Loaded {len(projects)} projects from Excel file")
            return projects
            
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return []
    
    def select_random_projects(self, projects: List[str], num_to_select: int) -> List[str]:
        """
        Randomly select projects from the list.
        
        Args:
            projects: List of all projects
            num_to_select: Number of projects to select
        
        Returns:
            List of randomly selected projects
        """
        if num_to_select > len(projects):
            print(f"Warning: Requested {num_to_select} projects but only {len(projects)} available")
            num_to_select = len(projects)
        
        if num_to_select <= 0:
            return []
        
        selected = random.sample(projects, num_to_select)
        return selected
    
    def get_recommended_sample_size(self, total_projects: int) -> dict:
        """
        Get recommended number of projects to document based on best practices.
        
        Args:
            total_projects: Total number of projects
        
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'total_projects': total_projects,
            'conservative': 0,
            'moderate': 0,
            'aggressive': 0,
            'notes': []
        }
        
        if total_projects <= 10:
            recommendations['conservative'] = total_projects
            recommendations['moderate'] = total_projects
            recommendations['aggressive'] = total_projects
            recommendations['notes'].append("Document all projects for small portfolios")
            
        elif total_projects <= 25:
            recommendations['conservative'] = min(total_projects, 15)
            recommendations['moderate'] = min(total_projects, 12)
            recommendations['aggressive'] = min(total_projects, 8)
            recommendations['notes'].append("Small portfolio - document majority of projects")
            
        elif total_projects <= 50:
            recommendations['conservative'] = min(total_projects, 25)
            recommendations['moderate'] = min(total_projects, 18)
            recommendations['aggressive'] = min(total_projects, 12)
            recommendations['notes'].append("Medium portfolio - 25-50% documentation typical")
            
        elif total_projects <= 100:
            recommendations['conservative'] = min(total_projects, 35)
            recommendations['moderate'] = min(total_projects, 25)
            recommendations['aggressive'] = min(total_projects, 15)
            recommendations['notes'].append("Large portfolio - 15-35% documentation common")
            
        elif total_projects <= 200:
            recommendations['conservative'] = min(total_projects, 50)
            recommendations['moderate'] = min(total_projects, 35)
            recommendations['aggressive'] = min(total_projects, 20)
            recommendations['notes'].append("Very large portfolio - 10-25% documentation")
            
        else:  # > 200 projects
            recommendations['conservative'] = min(total_projects, 75)
            recommendations['moderate'] = min(total_projects, 50)
            recommendations['aggressive'] = min(total_projects, 30)
            recommendations['notes'].append("Enterprise portfolio - 5-15% documentation may suffice")
        
        # Add general notes
        recommendations['notes'].extend([
            "Conservative: Lower audit risk, higher documentation cost",
            "Moderate: Balanced approach, most common selection",
            "Aggressive: Higher audit risk, lower documentation cost",
            "Consider project size, complexity, and credit value when selecting"
        ])
        
        return recommendations
    
    def randomize_projects(self, input_data: Union[str, List[str]], 
                          num_to_select: int = None, 
                          project_column: str = None,
                          recommendation_level: str = 'moderate') -> dict:
        """
        Main method to randomize project selection.
        
        Args:
            input_data: Either file path (string) or list of projects
            num_to_select: Number of projects to select (if None, uses recommendations)
            project_column: Column name for Excel files
            recommendation_level: 'conservative', 'moderate', or 'aggressive'
        
        Returns:
            Dictionary with selected projects and metadata
        """
        # Load projects
        if isinstance(input_data, str):
            projects = self.load_projects_from_excel(input_data, project_column)
        elif isinstance(input_data, list):
            projects = [str(p).strip() for p in input_data if str(p).strip()]
            print(f"Using provided list of {len(projects)} projects")
        else:
            raise ValueError("Input must be either file path (string) or list of projects")
        
        if not projects:
            return {'error': 'No projects found in input'}
        
        # Get recommendations
        recommendations = self.get_recommended_sample_size(len(projects))
        
        # Determine number to select
        if num_to_select is None:
            num_to_select = recommendations[recommendation_level]
            print(f"Using {recommendation_level} recommendation: {num_to_select} projects")
        
        # Select random projects
        selected_projects = self.select_random_projects(projects, num_to_select)
        
        return {
            'total_projects': len(projects),
            'selected_count': len(selected_projects),
            'selected_projects': selected_projects,
            'recommendations': recommendations,
            'selection_percentage': round((len(selected_projects) / len(projects)) * 100, 1)
        }

def main():
    """Command line interface for the randomizer."""
    parser = argparse.ArgumentParser(description='R&D Tax Credit Project Randomizer')
    parser.add_argument('input', help='Excel file path or use --list for manual input')
    parser.add_argument('-n', '--number', type=int, help='Number of projects to select')
    parser.add_argument('-c', '--column', help='Excel column name containing projects')
    parser.add_argument('-l', '--level', choices=['conservative', 'moderate', 'aggressive'], 
                       default='moderate', help='Recommendation level')
    parser.add_argument('-s', '--seed', type=int, help='Random seed for reproducible results')
    parser.add_argument('--list', action='store_true', help='Use manual list input instead of Excel')
    
    args = parser.parse_args()
    
    randomizer = RDProjectRandomizer(seed=args.seed)
    
    try:
        if args.list:
            print("Enter projects one per line (press Ctrl+C when done):")
            projects = []
            try:
                while True:
                    project = input().strip()
                    if project:
                        projects.append(project)
            except KeyboardInterrupt:
                print(f"\nProcessing {len(projects)} projects...")
            
            result = randomizer.randomize_projects(projects, args.number, 
                                                 recommendation_level=args.level)
        else:
            result = randomizer.randomize_projects(args.input, args.number, 
                                                  args.column, args.level)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            return
        
        # Display results
        print(f"\n{'='*50}")
        print(f"R&D PROJECT SELECTION RESULTS")
        print(f"{'='*50}")
        print(f"Total Projects: {result['total_projects']}")
        print(f"Selected: {result['selected_count']} ({result['selection_percentage']}%)")
        print(f"\nSelected Projects:")
        print("-" * 30)
        for i, project in enumerate(result['selected_projects'], 1):
            print(f"{i:2d}. {project}")
        
        print(f"\n{'='*50}")
        print("DOCUMENTATION RECOMMENDATIONS")
        print(f"{'='*50}")
        recs = result['recommendations']
        print(f"Conservative approach: {recs['conservative']} projects")
        print(f"Moderate approach:     {recs['moderate']} projects")
        print(f"Aggressive approach:   {recs['aggressive']} projects")
        
        print(f"\nNotes:")
        for note in recs['notes']:
            print(f"• {note}")
            
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Example 1: Using a list of projects
    sample_projects = [
        "AI Chatbot Development",
        "Database Optimization Engine",
        "Mobile App Security Framework",
        "IoT Sensor Network",
        "Machine Learning Model Training",
        "Cloud Migration Tool",
        "API Gateway Enhancement",
        "Blockchain Integration",
        "Data Analytics Dashboard",
        "Automated Testing Suite"
    ]
    
    randomizer = RDProjectRandomizer(seed=42)  # Use seed for reproducible results
    
    print("EXAMPLE: Random selection from sample projects")
    result = randomizer.randomize_projects(sample_projects, recommendation_level='moderate')
    
    print(f"Total: {result['total_projects']} projects")
    print(f"Selected {result['selected_count']} projects:")
    for project in result['selected_projects']:
        print(f"• {project}")
    
    print(f"\nRecommendations for {result['total_projects']} projects:")
    recs = result['recommendations']
    print(f"Conservative: {recs['conservative']}, Moderate: {recs['moderate']}, Aggressive: {recs['aggressive']}")
    
    # Uncomment to run command line interface
    # main()