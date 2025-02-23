# Response Handling for deepseek-r1-671b

## Overview
This document captures the response handling behavior of the deepseek-r1-671b model via venice.ai API, with focus on think tag processing and streaming responses.

## Think Tag Behavior
1. Format:
   - Think tags appear as `<think>` and `</think>` markers
   - Always at the start of model responses
   - Contains model's internal reasoning process
   - Must be stripped from final output

2. Processing Requirements:
   - Buffer initial chunks to detect think tags
   - Handle split tags across multiple chunks
   - Remove tags while preserving content
   - Track think tag state during streaming

3. Common Patterns:
   - Think content typically includes:
     * Task analysis
     * Planning steps
     * Quality checks
     * Word count monitoring
   - Tags are properly nested
   - Content after tags is the final output

## Test Results
The model's response pattern shows:

1. Response Structure:
   - Starts with `<think>` tag in first delta
   - Content is streamed in small chunks via delta updates
   - Each chunk is a JSON object with model metadata
   - Final chunk has "finish_reason": "stop"
   - Usage statistics provided at end of stream

2. Think Tag Pattern:
   - `<think>` appears at start of response
   - Contains model's reasoning process
   - Need to handle tag removal in streaming context

3. API Response Format:
   - OpenAI-compatible streaming format
   - Each chunk contains:
     - id: unique response ID
     - object: "chat.completion.chunk"
     - created: timestamp
     - model: "deepseek-r1-671b"
     - choices: array with delta updates
     - usage: null (except final chunk)

## Recommendations
1. Response Processing:
   - Buffer initial chunks to detect and handle think tags
   - Stream content after think tag processing
   - Monitor finish_reason for stream completion
   - Track usage statistics from final chunk

2. Think Tag Handling:
   - Option 1: Buffer until think section complete, then stream rest
   - Option 2: Mark think section in UI but stream everything
   - Option 3: Provide both raw and processed streams

3. Error Handling:
   - Monitor response status codes
   - Handle rate limits (x-ratelimit-* headers)
   - Implement retry logic for failed requests
   - Validate response format before processing
