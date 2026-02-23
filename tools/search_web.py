"""
title: Web Search Tool
author: Personal AI Agent
version: 2.0.0
description: Real-time web search using DuckDuckGo with URLs and snippets
"""

from duckduckgo_search import DDGS
from datetime import datetime


class Tools:
    def __init__(self):
        pass

    def search_web(self, query: str, max_results: int = 5) -> str:
        """
        Searches the web in real-time using DuckDuckGo.
        Returns URLs, titles, and content snippets.

        :param query: The search term
        :param max_results: Number of results to return (default: 5)
        :return: Formatted search results with URLs
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return f"No results found for '{query}'."

            formatted_results = []
            formatted_results.append(f"🔍 Search results for: {query}")
            formatted_results.append(f"⏰ Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            formatted_results.append("\n" + "="*60 + "\n")

            for idx, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('href', 'No URL')
                snippet = result.get('body', 'No description')

                formatted_results.append(f"{idx}. {title}")
                formatted_results.append(f"   🔗 {url}")
                formatted_results.append(f"   {snippet}")
                formatted_results.append("")

            return "\n".join(formatted_results)

        except Exception as e:
            return f"❌ Error searching: {str(e)}"
