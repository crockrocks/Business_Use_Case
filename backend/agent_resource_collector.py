from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import json
from typing import List, Dict, Any
import requests
from config import Config

class ResourceCollector:
    def __init__(self):
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self) -> ChatGroq:
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

    def search_kaggle_datasets(self, query: str) -> List[Dict[str, str]]:
        return [
            {
                "title": f"Dataset related to {query}",
                "url": f"https://www.kaggle.com/datasets?search={query}"
            }
        ]

    def search_huggingface_models(self, query: str) -> List[Dict[str, str]]:
        try:
            url = f"https://huggingface.co/api/models?search={query}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            models = response.json()[:3] 
            return [
                {
                    "title": model.get("modelId", ""),
                    "url": f"https://huggingface.co/{model.get('modelId', '')}"
                }
                for model in models
            ]
        except Exception:
            return []

    def search_research_papers(self, query: str) -> List[Dict[str, str]]:
        return [
            {
                "title": f"Research paper related to {query}",
                "url": f"https://scholar.google.com/scholar?q={query}"
            }
        ]

    def collect_resources(self, use_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        resources = {}
        
        for use_case in use_cases:
            use_case_title = use_case.get('title', '')
            if not use_case_title:
                continue
                
            search_query = self._create_search_query(use_case)
            resources[use_case_title] = {
                "datasets": self.search_kaggle_datasets(search_query),
                "models": self.search_huggingface_models(search_query),
                "research_papers": self.search_research_papers(search_query),
                "technical_requirements": self._generate_technical_requirements(use_case),
                "implementation_guidelines": self._generate_implementation_guidelines(use_case)
            }
        return resources

    def _create_search_query(self, use_case: Dict[str, Any]) -> str:
        title = use_case.get('title', '')
        description = use_case.get('description', '')
        technical_reqs = use_case.get('technical_requirements', '')
        query_parts = [
            word for word in f"{title} {description} {technical_reqs}".split()
            if len(word) > 3 
        ]
        
        return " ".join(query_parts[:8]) 

    def _generate_technical_requirements(self, use_case: Dict[str, Any]) -> List[str]:
        try:
            prompt_template = PromptTemplate(
                template="""
                For the following AI/ML use case, list the specific technical requirements:
                Use Case: {use_case}
                
                Consider:
                1. Required AI/ML models
                2. Computing resources
                3. Data requirements
                4. Integration points
                
                Return as a JSON array of strings.
                """,
                input_variables=["use_case"]
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            response = chain.invoke({"use_case": json.dumps(use_case)})
            
            return json.loads(response['text'])
        except Exception:
            return []

    def _generate_implementation_guidelines(self, use_case: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt_template = PromptTemplate(
                template="""
                Create implementation guidelines for the following AI/ML use case:
                Use Case: {use_case}
                
                Include:
                1. Development phases
                2. Key milestones
                3. Potential challenges
                4. Success metrics
                
                Return as a JSON object.
                """,
                input_variables=["use_case"]
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            response = chain.invoke({"use_case": json.dumps(use_case)})
            
            return json.loads(response['text'])
        except Exception:
            return {}

def collect_resources(use_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    collector = ResourceCollector()
    return collector.collect_resources(use_cases)
