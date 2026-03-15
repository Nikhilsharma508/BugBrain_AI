# src/agents/triage_agent.py — Severity & Team Classification Agent
#
# PURPOSE:
#   Determines the severity level (P1–P4) and suggests the owning team
#   for a bug report based on:
#     - The structured extraction output
#     - Severity policy rules from src/policies/severity_policy.yaml
#     - Team routing rules from src/policies/team_routing.yaml
#
# APPROACH:
#   Loads policy YAML files and includes them in the LLM prompt context.
#   The LLM acts as a classifier, applying the policy rules to the
#   extracted technical details.
#
# KEY CLASS:
#   TriageAgent — with methods like:
#     - classify(extraction_result: TriageResult) → TriageResult
#       (enriches the result with severity and suggested_owner)
#
# TODO:
#   - Load policy YAML files at init
#   - Build prompt with policy context
#   - Implement classification logic
#   - Add fallback for unknown categories

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import yaml
