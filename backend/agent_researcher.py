import json
import requests
from config import Config
from typing import Dict, Any, List
import re

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    text = ' '.join(text.split())
    if text and not text.endswith(('.', '!', '?')):
        text = text + '.'
    return text

def extract_complete_finding(result: Dict[str, Any]) -> str:
    texts = []
    if snippet := result.get("snippet"):
        texts.append(snippet)
    if title := result.get("title"):
        title = re.sub(r'\s*[-|]\s*.*$', '', title)
        texts.append(title)
    if description := result.get("description"):
        texts.append(description)
    combined_text = ' '.join(texts)
    sentences = set(re.split(r'[.!?]+', combined_text))
    clean_sentences = [clean_text(s) for s in sentences if s.strip()]
    return ' '.join(clean_sentences)

def summarize_findings(findings: List[str]) -> List[str]:
    summarized = []
    for finding in findings:
        if len(finding.split()) < 5:
            continue
        if finding.count('.') > 3:
            sentences = re.split(r'[.!?]+', finding)
            finding = '. '.join(s.strip() for s in sentences[:3] if len(s.strip()) > 20) + '.'  
        summarized.append(clean_text(finding))  
    return summarized

def research_company_and_industry(company_name: str, industry: str) -> Dict[str, Any]:
    try:
        serper_api_key = Config.SERPER_API_KEY
        if not serper_api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")
        searches = [
            f"{company_name} {industry} competitive advantage analysis",
            f"{company_name} {industry} market position research",
            f"{company_name} {industry} strategic analysis"
        ]
        
        all_results = []
        for query in searches:
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": query,
                "num": 5 
            })
            headers = {
                'X-API-KEY': serper_api_key,
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data=payload, timeout=30)
            response.raise_for_status()
            search_results = response.json()
            all_results.extend(search_results.get("organic", []))
        raw_findings = [extract_complete_finding(result) for result in all_results]
        key_findings = summarize_findings(raw_findings)
        seen = set()
        unique_findings = []
        for finding in key_findings:
            if finding not in seen:
                seen.add(finding)
                unique_findings.append(finding)

        structured_data = {
            "company_name": company_name,
            "industry": industry,
            "market_analysis": {
                "key_findings": unique_findings[:5],  # Limit to top 5 most relevant findings
                "sources": list(set(result.get("link") for result in all_results if result.get("link")))
            },
            "strategic_focus": extract_strategic_focus(all_results),
            "market_trends": extract_market_trends(all_results)
        }
        if not structured_data["market_analysis"]["key_findings"]:
            raise ValueError("No valid key findings were extracted")
            
        return structured_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Research failed: {str(e)}")

def extract_strategic_focus(results: list) -> list:
    focus_areas = set()
    keywords = ["innovation", "technology", "sustainability", "efficiency", 
                "customer experience", "digital transformation", "operations", 
                "supply chain", "quality", "research"]

    for result in results:
        snippet = result.get("snippet", "").lower()
        for keyword in keywords:
            if keyword in snippet:
                focus_areas.add(keyword.title())

    return list(focus_areas) if focus_areas else ["Operations", "Innovation", "Customer Experience"]

def extract_market_trends(results: list) -> list:
    trends = []
    for result in results:
        snippet = result.get("snippet", "")
        if any(keyword in snippet.lower() for keyword in ["trend", "growth", "future", "emerging", "innovation"]):
            trends.append(snippet)
    return trends[:5]