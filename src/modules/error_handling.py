"""
Error handling module for the Deep Research AI system.

This module provides comprehensive error handling, recovery strategies,
graceful degradation, and user-friendly error messaging.
"""

import logging
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, TypeVar

from ..config import Config
from ..llm_client import LLMClient
from ..prompts.error_prompts import (
    ERROR_ANALYSIS_PROMPT,
    GRACEFUL_DEGRADATION_PROMPT,
    USER_ERROR_MESSAGE_PROMPT,
    RETRY_STRATEGY_PROMPT,
    ERROR_RECOVERY_PROMPT,
    FALLBACK_CONTENT_PROMPT,
    SYSTEM_HEALTH_PROMPT,
)


# Set up logging
logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ComponentType(Enum):
    """System component types."""
    QUERY_UNDERSTANDING = "query_understanding"
    WEB_SEARCH = "web_search"
    REASONING_ENGINE = "reasoning_engine"
    VERIFICATION = "verification"
    CITATION = "citation"
    OUTPUT_GENERATION = "output_generation"
    LLM_CLIENT = "llm_client"
    ORCHESTRATOR = "orchestrator"


@dataclass
class ErrorContext:
    """Context information for an error."""
    component: ComponentType
    operation: str
    query: str | None = None
    partial_results: dict | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    attempt_number: int = 1
    max_attempts: int = 3


@dataclass
class ErrorRecord:
    """Record of an error occurrence."""
    error_type: str
    error_message: str
    context: ErrorContext
    severity: ErrorSeverity
    traceback_str: str | None = None
    recovery_attempted: bool = False
    recovery_successful: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


class ResearchError(Exception):
    """Base exception for research system errors."""
    
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        recoverable: bool = True,
        context: ErrorContext | None = None
    ):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.recoverable = recoverable
        self.context = context


class QueryError(ResearchError):
    """Error in query understanding."""
    pass


class SearchError(ResearchError):
    """Error in web search."""
    pass


class ReasoningError(ResearchError):
    """Error in reasoning engine."""
    pass


class VerificationError(ResearchError):
    """Error in verification."""
    pass


class CitationError(ResearchError):
    """Error in citation generation."""
    pass


class LLMError(ResearchError):
    """Error in LLM communication."""
    pass


class RateLimitError(ResearchError):
    """Rate limit exceeded error."""
    pass


# Type variable for generic retry function
T = TypeVar('T')


class ErrorHandler:
    """
    Comprehensive error handling for the research system.
    
    Provides:
    - Error analysis and diagnosis
    - Graceful degradation
    - Retry strategies
    - Recovery orchestration
    - User-friendly error messages
    """
    
    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the ErrorHandler.
        
        Args:
            config: Configuration object. Uses default if not provided.
        """
        self.config = config or Config()
        self.llm_client = LLMClient(self.config.llm_config)
        self.error_history: list[ErrorRecord] = []
        self.max_history = 100
    
    def record_error(
        self,
        error: Exception,
        context: ErrorContext,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ) -> ErrorRecord:
        """
        Record an error occurrence.
        
        Args:
            error: The exception that occurred
            context: Error context
            severity: Error severity level
            
        Returns:
            ErrorRecord object
        """
        record = ErrorRecord(
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            severity=severity,
            traceback_str=traceback.format_exc()
        )
        
        self.error_history.append(record)
        
        # Trim history if needed
        if len(self.error_history) > self.max_history:
            self.error_history = self.error_history[-self.max_history:]
        
        # Log the error
        log_level = {
            ErrorSeverity.INFO: logging.INFO,
            ErrorSeverity.WARNING: logging.WARNING,
            ErrorSeverity.ERROR: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(severity, logging.ERROR)
        
        logger.log(
            log_level,
            f"Error in {context.component.value}: {record.error_message}"
        )
        
        return record
    
    async def analyze_error(
        self,
        error: Exception,
        context: ErrorContext
    ) -> dict[str, Any]:
        """
        Analyze an error and suggest recovery strategies.
        
        Args:
            error: The exception to analyze
            context: Error context
            
        Returns:
            Dictionary with analysis and recovery suggestions
        """
        prompt = ERROR_ANALYSIS_PROMPT.format(
            error_type=type(error).__name__,
            error_message=str(error),
            context=str(context),
            component=context.component.value
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception as e:
            # Fallback if LLM analysis fails
            logger.warning(f"Error analysis failed: {e}")
            return {
                "analysis": {
                    "root_cause": "Unknown",
                    "impact_level": "medium",
                    "is_recoverable": True
                },
                "user_message": "An error occurred. Please try again.",
                "recovery_strategies": []
            }
    
    async def get_degraded_response(
        self,
        operation: str,
        partial_results: dict | None,
        missing_components: list[str]
    ) -> dict[str, Any]:
        """
        Get a gracefully degraded response when full operation fails.
        
        Args:
            operation: The failed operation
            partial_results: Any partial results available
            missing_components: Components that failed
            
        Returns:
            Dictionary with degraded response strategy
        """
        prompt = GRACEFUL_DEGRADATION_PROMPT.format(
            operation=operation,
            partial_results=str(partial_results) if partial_results else "None",
            missing_components=str(missing_components)
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            return {
                "degraded_response": {
                    "can_provide_partial": partial_results is not None,
                    "available_results": partial_results,
                    "quality_reduction": 0.5
                },
                "user_communication": {
                    "message": "We encountered some issues but have partial results.",
                    "limitations_explained": missing_components
                }
            }
    
    async def generate_user_message(
        self,
        error: Exception,
        user_action: str,
        severity: ErrorSeverity
    ) -> dict[str, Any]:
        """
        Generate a user-friendly error message.
        
        Args:
            error: The exception
            user_action: What the user was trying to do
            severity: Error severity
            
        Returns:
            Dictionary with user-friendly message
        """
        prompt = USER_ERROR_MESSAGE_PROMPT.format(
            error_type=type(error).__name__,
            technical_message=str(error),
            user_action=user_action,
            severity=severity.value
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            return {
                "user_message": {
                    "headline": "Something went wrong",
                    "explanation": "We encountered an issue processing your request.",
                    "what_to_do": "Please try again. If the problem persists, try rephrasing your query.",
                    "tone": "apologetic"
                },
                "severity_indicator": severity.value
            }
    
    async def get_retry_strategy(
        self,
        operation: str,
        failure_reason: str,
        attempt_number: int,
        context: dict
    ) -> dict[str, Any]:
        """
        Determine optimal retry strategy.
        
        Args:
            operation: Failed operation
            failure_reason: Why it failed
            attempt_number: Current attempt number
            context: Operation context
            
        Returns:
            Dictionary with retry strategy
        """
        prompt = RETRY_STRATEGY_PROMPT.format(
            operation=operation,
            failure_reason=failure_reason,
            attempt_number=attempt_number,
            context=str(context)
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            # Default retry strategy
            return {
                "retry_decision": {
                    "should_retry": attempt_number < 3,
                    "max_attempts": 3,
                    "current_attempt": attempt_number
                },
                "timing": {
                    "delay_seconds": attempt_number * 2,
                    "backoff_strategy": "exponential"
                },
                "modifications": {
                    "modify_request": False
                }
            }
    
    async def orchestrate_recovery(
        self,
        current_state: dict,
        error_chain: list[ErrorRecord]
    ) -> dict[str, Any]:
        """
        Orchestrate recovery from error state.
        
        Args:
            current_state: Current system state
            error_chain: Chain of errors that occurred
            
        Returns:
            Dictionary with recovery plan
        """
        error_chain_text = "\n".join([
            f"- {e.error_type}: {e.error_message}"
            for e in error_chain
        ])
        
        prompt = ERROR_RECOVERY_PROMPT.format(
            current_state=str(current_state),
            error_chain=error_chain_text,
            available_resources=str(list(ComponentType))
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            return {
                "state_assessment": {
                    "corruption_level": "partial"
                },
                "recovery_plan": [
                    {
                        "step": 1,
                        "action": "Reset to clean state",
                        "fallback": "Manual intervention required"
                    }
                ]
            }
    
    async def generate_fallback_content(
        self,
        query: str,
        available_info: dict | None,
        failed_sources: list[str],
        cached_data: dict | None = None
    ) -> dict[str, Any]:
        """
        Generate fallback content when primary sources fail.
        
        Args:
            query: Original query
            available_info: Any available information
            failed_sources: Sources that failed
            cached_data: Any cached data available
            
        Returns:
            Dictionary with fallback content
        """
        prompt = FALLBACK_CONTENT_PROMPT.format(
            query=query,
            available_info=str(available_info) if available_info else "None",
            failed_sources=str(failed_sources),
            cached_data=str(cached_data) if cached_data else "None"
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            return {
                "fallback_content": {
                    "response": "Unable to complete the research at this time.",
                    "confidence": 0.0,
                    "completeness": 0.0
                },
                "limitations_disclosure": {
                    "what_is_missing": failed_sources,
                    "quality_impact": "significant"
                }
            }
    
    async def check_system_health(
        self,
        health_metrics: dict,
        performance_data: dict
    ) -> dict[str, Any]:
        """
        Check overall system health.
        
        Args:
            health_metrics: Health metrics from components
            performance_data: Performance statistics
            
        Returns:
            Dictionary with health assessment
        """
        recent_errors = [
            {"type": e.error_type, "message": e.error_message}
            for e in self.error_history[-10:]
        ]
        
        prompt = SYSTEM_HEALTH_PROMPT.format(
            health_metrics=str(health_metrics),
            recent_errors=str(recent_errors),
            performance_data=str(performance_data)
        )
        
        try:
            result = await self.llm_client.call_json(prompt)
            return result
        except Exception:
            # Calculate simple health based on error rate
            error_count = len(self.error_history)
            health_score = max(0.0, 1.0 - (error_count / 100))
            
            return {
                "health_status": {
                    "overall": "healthy" if health_score > 0.7 else "degraded",
                    "score": health_score
                },
                "active_issues": [],
                "recommendations": []
            }
    
    async def retry_with_backoff(
        self,
        func: Callable[..., T],
        *args,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        **kwargs
    ) -> T:
        """
        Retry a function with exponential backoff.
        
        Args:
            func: Async function to retry
            *args: Positional arguments for func
            max_attempts: Maximum retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Backoff multiplier
            **kwargs: Keyword arguments for func
            
        Returns:
            Result from successful function call
            
        Raises:
            Last exception if all retries fail
        """
        import asyncio
        
        last_exception = None
        delay = initial_delay
        
        for attempt in range(1, max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < max_attempts:
                    logger.warning(
                        f"Attempt {attempt} failed: {e}. Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
        
        raise last_exception
    
    def get_error_summary(self) -> dict[str, Any]:
        """
        Get a summary of recent errors.
        
        Returns:
            Dictionary with error statistics and recent errors
        """
        if not self.error_history:
            return {
                "total_errors": 0,
                "by_severity": {},
                "by_component": {},
                "recent_errors": []
            }
        
        by_severity = {}
        by_component = {}
        
        for record in self.error_history:
            sev = record.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1
            
            comp = record.context.component.value
            by_component[comp] = by_component.get(comp, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "by_severity": by_severity,
            "by_component": by_component,
            "recent_errors": [
                {
                    "type": e.error_type,
                    "message": e.error_message,
                    "component": e.context.component.value,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in self.error_history[-5:]
            ]
        }
    
    def clear_error_history(self) -> None:
        """Clear the error history."""
        self.error_history = []
        logger.info("Error history cleared")


# Module singleton instance
error_handler = ErrorHandler()
