"""
title: Web Search Tool
author: Personal AI Agent
version: 1.0.0
description: Searches the web using DuckDuckGo API
"""

import httpx


class Tools:
    def __init__(self):
        pass

    def search_web(self, query: str) -> str:
        """
        Searches the web using DuckDuckGo.

        :param query: The search term
        :return: Search results
        """
        try:
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1}
            r = httpx.get(url, params=params, timeout=10)
            data = r.json()

            results = []
            for item in data.get("RelatedTopics", [])[:5]:
                if "Text" in item:
                    results.append(item["Text"])
                elif "Topics" in item:
                    for subitem in item["Topics"][:3]:
                        if "Text" in subitem:
                            results.append(subitem["Text"])

            if not results:
                # Try abstract if no related topics
                abstract = data.get("AbstractText", "")
                if abstract:
                    results.append(abstract)

            return "\n\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Error searching: {str(e)}"
