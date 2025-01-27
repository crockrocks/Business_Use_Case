from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import logging
import sys
from agent_researcher import research_company_and_industry
from agent_use_case_generator import generate_use_cases
from agent_resource_collector import collect_resources

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_research.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class ReportGenerator:
    def __init__(self, company_name: str, industry: str):
        self.company_name = company_name
        self.industry = industry
        self.output_dir = Path("reports")
        self._clear_reports_directory()
        self.output_dir.mkdir(exist_ok=True)

    def _clear_reports_directory(self) -> None:
        try:
            if self.output_dir.exists():
                shutil.rmtree(self.output_dir)
            logger.info("Reports directory cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing reports directory: {str(e)}")
            raise

    def generate_report(self) -> dict:
        try:
            logger.info(f"Starting report generation for {self.company_name}")
            research_data = self._conduct_research()
            use_cases = self._generate_use_cases(research_data)
            resources = self._collect_resources(use_cases)
            report = self._compile_report(research_data, use_cases, resources)
            self._save_report(report)
            return report
            
        except Exception as e:
            logger.error(f"Error in report generation: {str(e)}")
            raise

    def _conduct_research(self) -> dict:
        try:
            logger.info("Starting research phase")
            research_data = research_company_and_industry(self.company_name, self.industry)
            logger.info("Research phase completed successfully")
            return research_data
        except Exception as e:
            logger.error(f"Research phase failed: {str(e)}")
            raise

    def _generate_use_cases(self, research_data: dict) -> list:
        try:
            logger.info("Starting use case generation phase")
            use_cases = generate_use_cases(self.company_name, self.industry, research_data)
            logger.info("Use case generation completed successfully")
            return use_cases
        except Exception as e:
            logger.error(f"Use case generation failed: {str(e)}")
            raise

    def _collect_resources(self, use_cases: list) -> dict:
        try:
            logger.info("Starting resource collection phase")
            resources = collect_resources(use_cases)
            logger.info("Resource collection completed successfully")
            return resources
        except Exception as e:
            logger.error(f"Resource collection failed: {str(e)}")
            raise

    def _compile_report(self, research_data: dict, use_cases: list, resources: dict) -> dict:
        return {
            "metadata": {
                "company_name": self.company_name,
                "industry": self.industry,
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "research_summary": research_data,
            "use_cases": use_cases,
            "resources": resources
        }

    def _save_report(self, report: dict) -> None:
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.company_name.lower().replace(' ', '_')}_{timestamp}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved successfully to {filepath}")
        except Exception as e:
            logger.error(f"Error saving report: {str(e)}")
            raise

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        industry = data.get('industry')
        
        if not company_name or not industry:
            return jsonify({
                'error': 'Both company name and industry are required'
            }), 400
        generator = ReportGenerator(company_name, industry)
        report = generator.generate_report()
        
        return jsonify({
            'status': 'success',
            'data': report
        })
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        reports_dir = Path("reports")
        reports = []
        
        if reports_dir.exists():
            for file in reports_dir.glob("*.json"):
                with open(file, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                    reports.append({
                        'filename': file.name,
                        'company_name': report_data['metadata']['company_name'],
                        'industry': report_data['metadata']['industry'],
                        'generated_at': report_data['metadata']['generated_at']
                    })
        
        return jsonify({
            'status': 'success',
            'data': reports
        })
        
    except Exception as e:
        logger.error(f"Error fetching reports: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/reports/<filename>', methods=['GET'])
def get_report(filename):
    try:
        report_path = Path("reports") / filename
        
        if not report_path.exists():
            return jsonify({
                'status': 'error',
                'error': 'Report not found'
            }), 404
            
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
            
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching report {filename}: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)