# Tool: suggest_tools_for_goal
# Original callable name might differ if aliased (e.g. vN versions)

def suggest_tools_for_goal_v3(goal_description: str, top_n: int = 5) -> dict:
    """
    (Version 3 - aliased as v2 for tests) Suggests relevant tools.
    Adds a specific bonus for 'make_http_request' if a URL is detected in the goal.
    """
    tool_name_internal = "suggest_tools_for_goal_v3"
    # print(f"Agent log ({tool_name_internal}): Called with goal='{goal_description[:100]}...'.")

    if not goal_description:
        # ... (empty goal handling) ...
        return {"success": False, "message": "Goal description cannot be empty.", "goal": goal_description, "suggestions": []}

    global _TOOL_DESCRIPTIONS, _AGENT_TOOL_CONCEPT_KEYWORDS
    if not _TOOL_DESCRIPTIONS:
        # ... (no descriptions handling) ...
        return {"success": False, "message": "No tool descriptions available.", "goal": goal_description, "suggestions": []}

    def tokenize(text: str) -> set[str]: # Same tokenizer as before
        if not text: return set()
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {
            "a", "an", "the", "is", "to", "and", "of", "it", "for", "in", "on", "with",
            "i", "me", "my", "myself", "want", "some", "new", "called", "current", "me", "all",
            "do", "can", "you", "please", "how", "what", "tell", "give"
        }
        return set(word for word in words if word not in stop_words and len(word) > 2)

    goal_keywords = tokenize(goal_description)
    if not goal_keywords:
        # ... (no keywords handling) ...
        return {"success": True, "message": "No effective keywords in goal.", "goal": goal_description, "suggestions": []}

    # Detect URL in goal for special bonus
    url_pattern = r"https?://[^\s'\"]+" # Simpler pattern for detection
    goal_has_url = bool(re.search(url_pattern, goal_description, re.IGNORECASE))
    if goal_has_url:
        print(f"Agent log ({tool_name_internal}): URL detected in goal description.")


    suggestions = []
    for tool_name_key in _TOOL_DESCRIPTIONS.keys():
        description = _TOOL_DESCRIPTIONS[tool_name_key]
        relevance_score = 0.0
        matching_keywords_details = {}
        
        tool_concepts = _AGENT_TOOL_CONCEPT_KEYWORDS.get(tool_name_key, set())
        concept_matches = goal_keywords.intersection(tool_concepts)
        if concept_matches:
            relevance_score += len(concept_matches) * 3.0
            matching_keywords_details["concept"] = list(concept_matches)
            
        tokenized_tool_name = tokenize(tool_name_key.replace("_", " "))
        name_matches = goal_keywords.intersection(tokenized_tool_name)
        if name_matches:
            relevance_score += len(name_matches) * 2.0
            matching_keywords_details["name"] = list(name_matches)
        
        tokenized_description = tokenize(description)
        desc_matches = goal_keywords.intersection(tokenized_description)
        if desc_matches:
            unique_desc_matches = desc_matches - name_matches - concept_matches
            relevance_score += len(unique_desc_matches) * 1.0
            if unique_desc_matches : matching_keywords_details["description"] = list(unique_desc_matches)

        # **NEW**: Apply bonus if URL detected in goal and tool is make_http_request
        if goal_has_url and tool_name_key == "make_http_request" and relevance_score > 0: # Only boost if it already has some relevance
            relevance_score += 5.0 # Significant bonus for URL presence
            print(f"Agent log ({tool_name_internal}): Applied URL bonus to 'make_http_request'. New score: {relevance_score}")
            if "bonus" not in matching_keywords_details: matching_keywords_details["bonus"] = []
            matching_keywords_details["bonus"].append("URL_in_goal")


        if relevance_score > 0:
            reason_parts = []
            all_matched_keywords_for_suggestion = set()
            if "concept" in matching_keywords_details: reason_parts.append(f"Concept ({', '.join(matching_keywords_details['concept'])})"); all_matched_keywords_for_suggestion.update(matching_keywords_details['concept'])
            if "name" in matching_keywords_details: reason_parts.append(f"Name ({', '.join(matching_keywords_details['name'])})"); all_matched_keywords_for_suggestion.update(matching_keywords_details['name'])
            if "description" in matching_keywords_details: reason_parts.append(f"Desc ({', '.join(matching_keywords_details['description'])})"); all_matched_keywords_for_suggestion.update(matching_keywords_details['description'])
            if "bonus" in matching_keywords_details: reason_parts.append(f"Bonus ({', '.join(matching_keywords_details['bonus'])})")

            final_reason = "; ".join(reason_parts) if reason_parts else "General keyword match."
            suggestions.append({
                "tool_name": tool_name_key, "description": description, "relevance_score": round(relevance_score, 2),
                "matching_keywords": sorted(list(all_matched_keywords_for_suggestion)), "reason": final_reason
            })

    suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
    final_suggestions = suggestions[:top_n]
    msg = f"Found {len(final_suggestions)} relevant tool suggestion(s) for the goal (out of {len(suggestions)} potential)."
    if not suggestions: msg = "No relevant tool suggestions found based on keyword matching."
    return {"success": True, "message": msg, "goal": goal_description, "suggestions": final_suggestions}
