"""
Error handling prompts for the Deep Research AI system.

These prompts handle error recovery, graceful degradation, and
user-friendly error message generation.
"""

# Error Analysis Prompt
ERROR_ANALYSIS_PROMPT = """You are an expert at analyzing and diagnosing system errors.

Your task is to analyze the error and suggest recovery strategies.

ERROR DETAILS:
- Type: {error_type}
- Message: {error_message}
- Context: {context}
- Component: {component}

Analyze the error and provide:

1. **Root Cause**: What likely caused this error
2. **Impact**: What functionality is affected
3. **Recovery Options**: Possible ways to recover
4. **Prevention**: How to prevent this in the future

Respond in JSON format:
{{
    "analysis": {{
        "root_cause": "most likely cause",
        "impact_level": "low|medium|high|critical",
        "affected_functionality": ["list of affected features"],
        "is_recoverable": true/false
    }},
    "recovery_strategies": [
        {{
            "strategy": "strategy name",
            "description": "how to implement",
            "success_likelihood": 0.0-1.0,
            "side_effects": ["potential side effects"]
        }}
    ],
    "user_message": "friendly message for the user",
    "technical_details": "detailed technical explanation",
    "prevention_measures": ["how to prevent in future"]
}}
"""

# Graceful Degradation Prompt
GRACEFUL_DEGRADATION_PROMPT = """You are an expert at designing graceful degradation strategies.

Your task is to suggest how to provide partial results when full functionality fails.

FAILED OPERATION: {operation}
PARTIAL RESULTS: {partial_results}
MISSING COMPONENTS: {missing_components}

Determine how to provide value despite the failure:

1. **Partial Delivery**: What can still be delivered?
2. **Quality Impact**: How is quality affected?
3. **User Communication**: How to explain the limitation?
4. **Workarounds**: Alternative approaches to try

Respond in JSON format:
{{
    "degraded_response": {{
        "can_provide_partial": true/false,
        "available_results": "what can be delivered",
        "missing_results": "what is unavailable",
        "quality_reduction": 0.0-1.0
    }},
    "user_communication": {{
        "message": "user-friendly explanation",
        "limitations_explained": ["list of limitations"],
        "workaround_suggestions": ["suggestions for user"]
    }},
    "alternative_approaches": [
        {{
            "approach": "alternative method",
            "feasibility": 0.0-1.0,
            "tradeoffs": ["tradeoffs"]
        }}
    ],
    "retry_recommendation": {{
        "should_retry": true/false,
        "retry_strategy": "how to retry",
        "delay_seconds": 0
    }}
}}
"""

# User Error Message Generation Prompt
USER_ERROR_MESSAGE_PROMPT = """You are an expert at crafting user-friendly error messages.

Your task is to create a helpful error message for the user.

ERROR INFORMATION:
- Error Type: {error_type}
- Technical Message: {technical_message}
- User Action: {user_action}
- Severity: {severity}

Create a user-friendly message that:

1. **Explains** what went wrong in simple terms
2. **Reassures** the user (if appropriate)
3. **Guides** them on what to do next
4. **Avoids** technical jargon

Respond in JSON format:
{{
    "user_message": {{
        "headline": "Brief, clear headline",
        "explanation": "What happened in plain language",
        "what_to_do": "Steps the user can take",
        "tone": "apologetic|informative|helpful"
    }},
    "actions": [
        {{
            "action": "action name",
            "description": "what it does",
            "button_text": "text for button/link"
        }}
    ],
    "show_technical_details": true/false,
    "severity_indicator": "info|warning|error|critical"
}}
"""

# Retry Strategy Prompt
RETRY_STRATEGY_PROMPT = """You are an expert at designing retry strategies for failed operations.

Your task is to determine the optimal retry strategy for the failed operation.

FAILED OPERATION: {operation}
FAILURE REASON: {failure_reason}
ATTEMPT NUMBER: {attempt_number}
OPERATION CONTEXT: {context}

Determine the best retry approach:

1. **Should Retry**: Is retrying worthwhile?
2. **Timing**: How long to wait before retry
3. **Modification**: Should the request be modified?
4. **Limit**: Maximum retry attempts

Respond in JSON format:
{{
    "retry_decision": {{
        "should_retry": true/false,
        "reason": "why or why not",
        "max_attempts": 0,
        "current_attempt": {attempt_number}
    }},
    "timing": {{
        "delay_seconds": 0,
        "backoff_strategy": "none|linear|exponential",
        "max_delay_seconds": 0
    }},
    "modifications": {{
        "modify_request": true/false,
        "suggested_changes": ["changes to make"],
        "reduce_scope": true/false
    }},
    "alternatives": [
        {{
            "alternative": "alternative approach",
            "when_to_use": "when this alternative is appropriate"
        }}
    ]
}}
"""

# Error Recovery Prompt
ERROR_RECOVERY_PROMPT = """You are an expert at recovering from errors in complex systems.

Your task is to orchestrate recovery from the current error state.

CURRENT STATE:
{current_state}

ERROR CHAIN:
{error_chain}

AVAILABLE RESOURCES:
{available_resources}

Plan the recovery:

1. **State Assessment**: What is the current system state?
2. **Recovery Path**: Steps to recover
3. **Data Salvage**: What data can be saved?
4. **State Restoration**: How to restore normal operation

Respond in JSON format:
{{
    "state_assessment": {{
        "corruption_level": "none|partial|severe",
        "salvageable_data": ["list of salvageable items"],
        "lost_data": ["list of lost items"]
    }},
    "recovery_plan": [
        {{
            "step": 1,
            "action": "action to take",
            "expected_outcome": "what should happen",
            "fallback": "what to do if this fails"
        }}
    ],
    "data_recovery": {{
        "recovered_items": ["items that can be recovered"],
        "recovery_method": "how to recover"
    }},
    "post_recovery": {{
        "verification_steps": ["how to verify recovery"],
        "monitoring_period": "how long to monitor",
        "success_indicators": ["indicators of successful recovery"]
    }}
}}
"""

# Fallback Content Generation Prompt
FALLBACK_CONTENT_PROMPT = """You are an expert at generating fallback content when primary sources fail.

Your task is to generate helpful fallback content based on available information.

ORIGINAL QUERY: {query}
AVAILABLE INFORMATION: {available_info}
FAILED SOURCES: {failed_sources}
CACHED DATA: {cached_data}

Generate fallback content that:

1. **Acknowledges** the limitation
2. **Provides** whatever information is available
3. **Suggests** alternatives
4. **Maintains** quality standards

Respond in JSON format:
{{
    "fallback_content": {{
        "response": "best possible response given limitations",
        "confidence": 0.0-1.0,
        "completeness": 0.0-1.0,
        "based_on": ["what information was used"]
    }},
    "limitations_disclosure": {{
        "what_is_missing": ["missing information"],
        "quality_impact": "how quality is affected",
        "reliability_note": "note about reliability"
    }},
    "next_steps": [
        {{
            "suggestion": "what user could try",
            "likelihood_of_success": 0.0-1.0
        }}
    ]
}}
"""

# System Health Check Prompt
SYSTEM_HEALTH_PROMPT = """You are an expert at assessing system health and diagnosing issues.

Your task is to analyze the system health metrics and identify issues.

HEALTH METRICS:
{health_metrics}

RECENT ERRORS:
{recent_errors}

PERFORMANCE DATA:
{performance_data}

Assess the system health:

1. **Overall Status**: System health rating
2. **Components**: Status of each component
3. **Issues**: Current and potential issues
4. **Recommendations**: What to do

Respond in JSON format:
{{
    "health_status": {{
        "overall": "healthy|degraded|unhealthy|critical",
        "score": 0.0-1.0
    }},
    "components": [
        {{
            "name": "component name",
            "status": "healthy|degraded|unhealthy",
            "issues": ["issues if any"]
        }}
    ],
    "active_issues": [
        {{
            "issue": "issue description",
            "severity": "low|medium|high|critical",
            "affected_functionality": ["affected features"]
        }}
    ],
    "recommendations": [
        {{
            "action": "recommended action",
            "priority": "immediate|soon|when_convenient",
            "impact": "expected impact"
        }}
    ]
}}
"""
