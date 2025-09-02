"""
Real-time Knowledge Integration for Prompt Enhancement
======================================================
Fetches current information to enhance prompts with up-to-date context
"""

import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class KnowledgeUpdater:
    """
    Integrates real-time knowledge into prompts for temporal accuracy
    """
    
    def __init__(self):
        self.search_api_url = "https://api.search.brave.com/res/v1/web/search"
        # You could also use other APIs like:
        # - SerpAPI for Google search
        # - Bing Search API
        # - DuckDuckGo API (free, no key required)
        
    async def should_fetch_current_info(self, prompt: str, context: str) -> bool:
        """
        Determine if the prompt needs current information
        """
        # Keywords that suggest need for current info
        time_sensitive_keywords = [
            "latest", "current", "today", "recent", "now", "2025", "2024",
            "news", "update", "trending", "modern", "state-of-the-art",
            "best practices", "new features", "release", "version"
        ]
        
        technical_terms_needing_updates = [
            "GPT-5", "GPT-4", "Claude", "Gemini", "AI model",
            "framework", "library", "API", "documentation",
            "benchmark", "performance", "optimization"
        ]
        
        prompt_lower = prompt.lower()
        
        # Check for time-sensitive keywords
        for keyword in time_sensitive_keywords:
            if keyword in prompt_lower:
                return True
                
        # Check for technical terms that change frequently
        for term in technical_terms_needing_updates:
            if term.lower() in prompt_lower:
                return True
                
        # Context-specific checks
        if context in ["coding", "technical", "analysis"]:
            # These contexts often need current info
            if any(word in prompt_lower for word in ["how to", "implement", "use", "setup"]):
                return True
                
        return False
    
    async def fetch_current_knowledge(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """
        Fetch current information from web search
        """
        try:
            # Using a simple DuckDuckGo instant answer API (no key needed)
            # For production, you'd want to use a proper search API
            
            # Simplified search using httpx
            async with httpx.AsyncClient(timeout=10.0) as client:
                # DuckDuckGo instant answer API
                ddg_url = "https://api.duckduckgo.com/"
                params = {
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1
                }
                
                response = await client.get(ddg_url, params=params)
                data = response.json()
                
                knowledge = {
                    "query": query,
                    "fetched_at": datetime.now().isoformat(),
                    "instant_answer": data.get("AbstractText", ""),
                    "source": data.get("AbstractSource", ""),
                    "url": data.get("AbstractURL", ""),
                    "related_topics": []
                }
                
                # Extract related topics
                for topic in data.get("RelatedTopics", [])[:max_results]:
                    if isinstance(topic, dict):
                        knowledge["related_topics"].append({
                            "text": topic.get("Text", ""),
                            "url": topic.get("FirstURL", "")
                        })
                
                return knowledge
                
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "fetched_at": datetime.now().isoformat()
            }
    
    async def enhance_with_current_knowledge(
        self,
        prompt: str,
        context: str,
        fetch_updates: bool = True
    ) -> Dict[str, Any]:
        """
        Enhance prompt with current knowledge if needed
        """
        enhancements = {
            "needs_current_info": False,
            "current_knowledge": None,
            "temporal_context": None,
            "suggested_additions": []
        }
        
        if not fetch_updates:
            return enhancements
            
        # Check if current info is needed
        if await self.should_fetch_current_info(prompt, context):
            enhancements["needs_current_info"] = True
            
            # Extract key terms to search for
            search_terms = self._extract_search_terms(prompt, context)
            
            # Fetch current knowledge for each term
            current_info = []
            for term in search_terms[:2]:  # Limit to 2 searches
                knowledge = await self.fetch_current_knowledge(term)
                if knowledge and not knowledge.get("error"):
                    current_info.append(knowledge)
            
            if current_info:
                enhancements["current_knowledge"] = current_info
                
                # Generate temporal context section
                enhancements["temporal_context"] = self._generate_temporal_context(
                    current_info,
                    datetime.now()
                )
                
                # Suggest additions to the prompt
                enhancements["suggested_additions"] = [
                    "Note: Information current as of " + datetime.now().strftime("%Y-%m-%d"),
                    "Consider recent developments in the field",
                    "Account for latest best practices and updates"
                ]
        
        return enhancements
    
    def _extract_search_terms(self, prompt: str, context: str) -> List[str]:
        """
        Extract key terms that should be searched for current info
        """
        terms = []
        
        # Context-specific term extraction
        if context == "coding":
            # Look for framework/library names
            tech_terms = ["react", "vue", "angular", "python", "javascript", 
                         "fastapi", "django", "tensorflow", "pytorch"]
            for term in tech_terms:
                if term in prompt.lower():
                    terms.append(f"{term} latest features 2025")
                    
        # Look for model names
        if "gpt" in prompt.lower():
            terms.append("GPT-5 capabilities 2025")
        if "claude" in prompt.lower():
            terms.append("Claude AI latest updates 2025")
            
        # Generic search for the main topic
        if not terms:
            # Simple extraction: first few meaningful words
            words = prompt.split()[:5]
            terms.append(" ".join(words) + " 2025")
            
        return terms
    
    def _generate_temporal_context(
        self,
        current_info: List[Dict],
        current_date: datetime
    ) -> str:
        """
        Generate a temporal context section for the prompt
        """
        context_parts = [
            f"### Temporal Context",
            f"Knowledge Cutoff: January 2025",
            f"Current Date: {current_date.strftime('%Y-%m-%d')}",
            f"Information Freshness: Real-time"
        ]
        
        if current_info:
            context_parts.append("\n### Current Information")
            for info in current_info:
                if info.get("instant_answer"):
                    context_parts.append(f"- {info['query']}: {info['instant_answer'][:200]}...")
                    if info.get("source"):
                        context_parts.append(f"  Source: {info['source']}")
                        
        return "\n".join(context_parts)


class SmartKnowledgeIntegration:
    """
    Intelligently decides when and how to integrate current knowledge
    """
    
    def __init__(self):
        self.updater = KnowledgeUpdater()
        self.cache = {}  # Simple cache for repeated queries
        
    async def should_enhance_with_knowledge(
        self,
        prompt: str,
        context: str,
        user_preference: Optional[str] = None
    ) -> bool:
        """
        Smart decision on whether to fetch current knowledge
        """
        # User preference overrides
        if user_preference == "always":
            return True
        if user_preference == "never":
            return False
            
        # Check prompt characteristics
        checks = {
            "is_time_sensitive": await self.updater.should_fetch_current_info(prompt, context),
            "is_technical": context in ["coding", "technical", "analysis"],
            "mentions_specific_tech": any(
                tech in prompt.lower() 
                for tech in ["gpt-5", "api", "framework", "latest", "current"]
            ),
            "is_long_form": len(prompt.split()) > 20  # Longer prompts might benefit
        }
        
        # Decision logic
        score = sum([
            checks["is_time_sensitive"] * 3,  # High weight
            checks["is_technical"] * 2,
            checks["mentions_specific_tech"] * 2,
            checks["is_long_form"] * 1
        ])
        
        return score >= 3  # Threshold for fetching
    
    async def integrate_knowledge(
        self,
        prompt: str,
        enhanced_prompt: str,
        context: str,
        user_preference: Optional[str] = None,
    ) -> str:
        """
        Integrate current knowledge into the enhanced prompt
        """
        # Check if we should fetch
        if not await self.should_enhance_with_knowledge(prompt, context, user_preference=user_preference):
            return enhanced_prompt
            
        # Get current knowledge
        knowledge = await self.updater.enhance_with_current_knowledge(
            prompt, 
            context,
            fetch_updates=True
        )
        
        if not knowledge.get("current_knowledge"):
            return enhanced_prompt
            
        # Find the right place to insert temporal context
        lines = enhanced_prompt.split("\n")
        
        # Look for where to insert (after first ### section or at beginning)
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith("###"):
                insert_index = i + 1
                break
                
        # Insert temporal context
        temporal_context = knowledge.get("temporal_context", "")
        if temporal_context:
            lines.insert(insert_index, temporal_context)
            lines.insert(insert_index + 1, "")  # Empty line for spacing
            
        return "\n".join(lines)
