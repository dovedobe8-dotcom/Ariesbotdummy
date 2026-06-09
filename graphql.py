"""
GraphQL utilities for fbchat-muqit.

This module provides utilities for handling GraphQL queries, responses,
and JSON parsing for Facebook's GraphQL API.
"""

import json
from typing import List, Dict, Any, Optional
from enum import IntEnum

import msgspec

# Use the existing logging and exception systems
from .logging.logger import get_logger
from .exception.errors import (
    FBChatError, 
    FacebookAPIError, 
    ValidationError, 
    handle_exceptions
)


class FacebookErrorCode(IntEnum):
    """Facebook API error codes."""
    NOT_LOGGED_IN = 1357001
    REFRESH_COOKIES = 1357004
    INVALID_PARAMS_1 = 1357031
    INVALID_PARAMS_2 = 1545010
    INVALID_PARAMS_3 = 1545003


class GraphQLError(msgspec.Struct, frozen=True, eq=False):
    """Represents a GraphQL error."""
    code: Optional[int] = None
    message: Optional[str] = None
    severity: Optional[str] = None


class QueryRequest(msgspec.Struct, frozen=True, eq=False):
    """Represents a GraphQL query request."""
    priority: int = 0
    query: Optional[str] = None
    query_id: Optional[str] = None
    doc: Optional[str] = None
    doc_id: Optional[str] = None
    query_params: Dict[str, Any] | None = dict()


class GraphQLProcessor:
    """Handles GraphQL query processing and response parsing."""
    
    def __init__(self):
        self.logger = get_logger()
        self.decoder = msgspec.json.Decoder()
    
    @handle_exceptions(ValidationError)
    def parse_json_stream(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse multiple concatenated JSON objects in a single string.
        
        Args:
            content: String containing one or more JSON objects
            
        Returns:
            List of parsed JSON objects
            
        Raises:
            ValidationError: If JSON parsing fails
        """
        if not content.strip():
            self.logger.trace("Empty content provided to parse_json_stream")
            return []
            
        results: List[Dict[str, Any]] = []
        content = content.strip()
        idx = 0

        self.logger.trace(f"Parsing JSON stream with {len(content)} characters")

        decoder = json.JSONDecoder()

        while idx < len(content):
            # Skip whitespace
            while idx < len(content) and content[idx].isspace():
                idx += 1
                
            if idx >= len(content):
                break
                
            try:
                obj, offset = decoder.raw_decode(content, idx)
                results.append(obj)
                idx += offset
                self.logger.trace(f"Successfully parsed JSON object at position {idx - offset}")
            except json.JSONDecodeError as e:
                self.logger.warning(f"JSON decode error at position {idx}: {e}")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error parsing JSON stream: {e}")
                raise ValidationError(
                    f"Failed to parse JSON stream: {e}",
                    details={'content_length': len(content), 'position': idx}
                ) from e

        self.logger.debug(f"Parsed {len(results)} JSON objects from stream")
        return results


    def process_normal_response(self, content: str)->Dict[str, Any]:
        try:
            cleaned_content = self.strip_json_cruft(content)
            return self.decoder.decode(cleaned_content)
        except (ValueError, msgspec.DecodeError) as e:
            raise ValidationError(
                "No valid JSON found in response",
                details={'content_preview': content[:100] + '...' if len(content) > 100 else content}
            ) from e
   

    @handle_exceptions(ValidationError)
    def strip_json_cruft(self, content: str) -> str:
        """
        Remove Facebook's JSON cruft like 'for(;;);' that precedes responses.
        
        Args:
            content: Raw response content
            
        Returns:
            Cleaned JSON string
            
        Raises:
            ValidationError: If no valid JSON is found
        """
        if not content:
            raise ValidationError("Empty content provided to strip_json_cruft")
            
        self.logger.trace(f"Stripping JSON cruft from {len(content)} character response")
        
        # Find the first opening brace
        try:
            start_idx = content.index("{")
            cleaned_content = content[start_idx:]
            cruft_length = start_idx
            if cruft_length > 0:
                cruft = content[:start_idx]
                self.logger.debug(f"Removed {cruft_length} characters of cruft: {cruft!r}")
            return cleaned_content
        except ValueError as e:
            raise ValidationError(
                "No valid JSON found in response",
                details={'content_preview': content[:100] + '...' if len(content) > 100 else content}
            ) from e

    def queries_to_json(self, *queries: QueryRequest) -> str:
        """
        Convert QueryRequest objects to JSON string format.
        
        Args:
            queries: Variable number of QueryRequest objects
            
        Returns:
            JSON string representation of queries
        """
        self.logger.debug(f"Converting {len(queries)} queries to JSON")
        
        rtn = {}
        for i, query in enumerate(queries):
            if query.query:
                rtn[f"q{i}"] = {
                    "priority": query.priority,
                    "q": query.query,
                    "query_params": query.query_params
                }
                self.logger.trace(f"Query {i}: GraphQL query with {len(query.query)} characters")
            elif query.query_id:
                rtn[f"q{i}"] = {
                    "query_id": query.query_id,
                    "query_params": query.query_params
                }
                self.logger.trace(f"Query {i}: Query ID {query.query_id}")
            elif query.doc:
                rtn[f"q{i}"] = {
                    "doc": query.doc,
                    "query_params": query.query_params
                }
                self.logger.trace(f"Query {i}: Document with {len(query.doc)} characters")
            elif query.doc_id:
                rtn[f"q{i}"] = {
                    "doc_id": query.doc_id,
                    "query_params": query.query_params
                }
                self.logger.trace(f"Query {i}: Document ID {query.doc_id}")
            
        json_str = json.dumps(rtn)
        self.logger.debug(f"Generated JSON query string with {len(json_str)} characters")
        return json_str



    @handle_exceptions(FacebookAPIError)
    def handle_payload_error(self, payload: Dict[str, Any]) -> None:
        """
        Handle Facebook API payload errors.
        
        Args:
            payload: The JSON payload to check for errors
            
        Raises:
            FacebookAPIError: For critical errors
        """
        if "error" not in payload:
            return
            
        error_code = payload["error"]
        self.logger.warning(f"Facebook payload error detected: {error_code}")
        
        error_details = {
            'error_code': error_code,
            'payload': payload
        }
        
        if error_code == FacebookErrorCode.NOT_LOGGED_IN:
            self.logger.error("Not logged into Facebook")
            raise FacebookAPIError(
                "Not logged in - please authenticate",
                error_code=error_code,
                details=error_details
            )
        elif error_code == FacebookErrorCode.REFRESH_COOKIES:
            self.logger.error("Cookies need to be refreshed")
            raise FacebookAPIError(
                "Please refresh your authentication cookies",
                error_code=error_code,
                details=error_details
            )
        elif error_code in (
            FacebookErrorCode.INVALID_PARAMS_1,
            FacebookErrorCode.INVALID_PARAMS_2,
            FacebookErrorCode.INVALID_PARAMS_3
        ):
            self.logger.error(f"Invalid parameters provided (error: {error_code})")
            raise FacebookAPIError(
                "Invalid parameters provided",
                error_code=error_code,
                details=error_details
            )
        else:
            self.logger.error(f"Unknown Facebook API error: {error_code}")
            raise FacebookAPIError(
                f"Facebook API error: {error_code}",
                error_code=error_code,
                details=error_details
            )

    @handle_exceptions(FacebookAPIError)
    def handle_graphql_errors(self, response: Dict[str, Any]) -> None:
        """
        Handle GraphQL-specific errors in the response.
        
        Args:
            response: GraphQL response object
            
        Raises:
            FacebookAPIError: For critical GraphQL errors
        """
        errors = []
        
        if response.get("error"):
            errors = [response["error"]]
        elif response.get("errors"):
            errors = response["errors"]
            
        if not errors:
            return
        
        self.logger.warning(f"GraphQL errors detected: {len(errors)} error(s)")
        
        # Process the first error (most critical)
        error_data = errors[0]
        error = GraphQLError(
            code=error_data.get("code"),
            message=error_data.get("message", "Unknown GraphQL error"),
            severity=error_data.get("severity")
        )
        
        self.logger.error(f"GraphQL error - Code: {error.code}, Message: {error.message}")
        
        # Raise exception for critical errors
        if error.severity == "CRITICAL" or error.code:
            raise FacebookAPIError(
                f"GraphQL error: {error.message}",
                error_code=error.code,
                details={
                    'graphql_errors': errors,
                    'severity': error.severity,
                    'response': response
                }
            )

    @handle_exceptions(FBChatError)
    def process_response(self, content: str) -> List[Optional[Dict[str, Any]]]:
        """
        Process Facebook's JSON response and extract structured data.
        
        Args:
            content: Raw JSON string from Facebook's API
            
        Returns:
            List of parsed response objects (None for invalid responses)
            
        Raises:
            FBChatError: If parsing fails or critical errors occur
        """
        if not content:
            self.logger.debug("Empty content provided to process_response")
            return []
        
        # self.logger.info(f"Processing Facebook response ({len(content)} characters)")
        
        # Clean the content and parse JSON objects
        try:
            cleaned_content = self.strip_json_cruft(content)
            parsed_objects = self.parse_json_stream(cleaned_content)
        except Exception as e:
            self.logger.error(f"Failed to parse response: {e}")
            raise FBChatError(f"Error parsing response: {e}") from e
        
        if not parsed_objects:
            self.logger.warning("No valid JSON objects found in response")
            return []
        
        self.logger.debug(f"Processing {len(parsed_objects)} parsed objects")
        
        results: List[Optional[Dict[str, Any]]] = []
        for obj_idx, obj in enumerate(parsed_objects):
            try:
                if "error_results" in obj:
                    continue
                # Handle payload-level errors
                self.handle_payload_error(obj)
                
                for key, value in obj.items():
                    self.logger.trace(f"Processing response key: {key}")
                    
                    # Handle GraphQL errors
                    self.handle_graphql_errors(value)
                    
                    # FIXED: Extract index and store result (matching original logic)
                    try:
                        index = int(key[1:])  # Extract numeric part (e.g., "q0" -> 0)
                            
                         # Extend results list if needed
                        while len(results) <= index:
                            results.append(None)
                            
                        # Store the result
                        if "response" in value:
                            results[index] = value["response"]
                            self.logger.trace(f"Extracted 'response' data for query {index}")
                        elif "data" in value:
                            results[index] = value["data"]
                            self.logger.trace(f"Extracted 'data' data for query {index}")
                        else:
                            results[index] = value
                            self.logger.trace(f"Using raw value for query {index}")
                                
                    except (ValueError, IndexError) as e:
                        self.logger.warning(f"Invalid query key format: {key} - {e}")
                        continue
                    else:
                        # Handle non-query keys if needed
                        self.logger.trace(f"Ignoring non-query key: {key}")
                        
            except FBChatError:
                raise  # Re-raise our custom exceptions (already logged)
            except Exception as e:
                self.logger.error(f"Error processing response object {obj_idx}: {e}")
                continue
        
        processed_count = sum(1 for r in results if r is not None)
        self.logger.info(f"Successfully processed {processed_count}/{len(results)} responses")
        
        return results


# Global processor instance for backward compatibility
_global_processor: Optional[GraphQLProcessor] = None


def get_processor() -> GraphQLProcessor:
    """Get the global GraphQL processor instance."""
    global _global_processor
    if _global_processor is None:
        _global_processor = GraphQLProcessor()
    return _global_processor


# Factory functions for creating QueryRequest objects
def from_query(query: str, params: Optional[Dict[str, Any]] = None) -> QueryRequest:
    """Create a QueryRequest from a GraphQL query string."""
    logger = get_logger()
    logger.trace(f"Creating QueryRequest from query ({len(query)} chars)")
    return QueryRequest(priority=0, query=query, query_params=params or {})


def from_query_id(query_id: str, params: Optional[Dict[str, Any]] = None) -> QueryRequest:
    """Create a QueryRequest from a query ID."""
    logger = get_logger()
    logger.trace(f"Creating QueryRequest from query_id: {query_id}")
    return QueryRequest(query_id=query_id, query_params=params or {})


def from_doc(doc: str, params: Optional[Dict[str, Any]] = None) -> QueryRequest:
    """Create a QueryRequest from a document string."""
    logger = get_logger()
    logger.trace(f"Creating QueryRequest from document ({len(doc)} chars)")
    return QueryRequest(doc=doc, query_params=params or {})


def from_doc_id(doc_id: str, params: Optional[Dict[str, Any]] = None) -> QueryRequest:
    """Create a QueryRequest from a document ID."""
    logger = get_logger()
    logger.trace(f"Creating QueryRequest from doc_id: {doc_id}")
    return QueryRequest(doc_id=doc_id, query_params=params or {})


# Backward compatibility functions (using global processor)
def parse_json_stream(content: str) -> List[Dict[str, Any]]:
    """Parse multiple concatenated JSON objects (backward compatibility)."""
    return get_processor().parse_json_stream(content)


def strip_json_cruft(content: str) -> str:
    """Remove JSON cruft from content (backward compatibility)."""
    return get_processor().strip_json_cruft(content)


def queries_to_json(*queries: QueryRequest) -> str:
    """Convert queries to JSON string (backward compatibility)."""
    return get_processor().queries_to_json(*queries)


def handle_payload_error(payload: Dict[str, Any]) -> None:
    """Handle payload errors (backward compatibility)."""
    return get_processor().handle_payload_error(payload)


def handle_graphql_error(response: Dict[str, Any]) -> None:
    """Handle GraphQL errors (backward compatibility - note: singular 'error' for compatibility)."""
    return get_processor().handle_graphql_errors(response)


def response_to_json(content: str) -> List[Optional[Dict[str, Any]]]:
    """Process response content (backward compatibility)."""
    return get_processor().process_response(content)
