import json
import logging
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_llm():
    try:
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        return ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=2000,
            timeout=30,
            max_retries=2,
        )
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise

def generate_use_cases(company_name: str, industry: str, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate AI/ML use cases based on research data."""
    try:
        logger.info(f"Generating use cases for {company_name}")
        llm = initialize_llm()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI/ML expert tasked with generating specific and actionable use cases. 
            Format your response as a valid JSON array where each object has the following structure:
            {{
                "title": "Use Case Title",
                "description": "Detailed description",
                "business_impact": "Expected impact on business",
                "technical_requirements": ["req1", "req2"],
                "complexity": "High/Medium/Low",
                "priority": "High/Medium/Low",
                "estimated_timeline": "X months",
                "success_metrics": ["metric1", "metric2"]
            }}"""),
            ("user", """Generate 5 AI/ML use cases for {company_name} in the {industry} industry.
            Consider the following research data: {research_data}
            
            Focus on:
            1. Customer experience enhancement
            2. Operational efficiency
            3. Product innovation
            4. Risk management
            5. Sustainability
            
            Return the use cases as a JSON array of objects using the structure specified above.""")
        ])
        chain = prompt | llm
        response = chain.invoke({
            "company_name": company_name,
            "industry": industry,
            "research_data": json.dumps(research_data)
        })
        content = response.content
        start_idx = content.find('[')
        end_idx = content.rfind(']') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No valid JSON array found in response")

        json_str = content[start_idx:end_idx]
        use_cases = json.loads(json_str)
        validated_use_cases = [validate_use_case(uc) for uc in use_cases]
        
        logger.info(f"Successfully generated {len(validated_use_cases)} use cases")
        return validated_use_cases
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {str(e)}")
        return [create_default_use_case(company_name, industry)]
    except Exception as e:
        logger.error(f"Error in generate_use_cases: {str(e)}")
        raise

def validate_use_case(use_case: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = {
        "title": str,
        "description": str,
        "business_impact": str,
        "technical_requirements": list,
        "complexity": str,
        "priority": str,
        "estimated_timeline": str,
        "success_metrics": list
    }
    
    validated = {}
    for field, field_type in required_fields.items():
        value = use_case.get(field)
        if not value or not isinstance(value, field_type):
            if field_type == list:
                validated[field] = []
            else:
                validated[field] = "Not specified"
        else:
            validated[field] = value

    valid_levels = ["High", "Medium", "Low"]
    validated["complexity"] = validated["complexity"] if validated["complexity"] in valid_levels else "Medium"
    validated["priority"] = validated["priority"] if validated["priority"] in valid_levels else "Medium"
    
    return validated

def create_default_use_case(company_name: str, industry: str) -> Dict[str, Any]:
    return {
        "title": f"AI-Powered Process Optimization for {company_name}",
        "description": f"Implement AI algorithms to optimize core business processes in the {industry} industry",
        "business_impact": "Improved efficiency and reduced operational costs",
        "technical_requirements": [
            "Machine Learning Platform",
            "Data Pipeline",
            "Integration APIs"
        ],
        "complexity": "Medium",
        "priority": "High",
        "estimated_timeline": "6 months",
        "success_metrics": [
            "Process efficiency improvement",
            "Cost reduction",
            "Employee productivity increase"
        ]
    }