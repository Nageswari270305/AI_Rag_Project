JUDGE_RUBRIC = """
Evaluate the quality of a legal contract question-answer pair.

Score the answer from 1 to 10.

Consider:

1. Correctness
- Is the answer correct according to the contract context?

2. Faithfulness
- Are the important claims supported by the provided context?

3. Relevance
- Does the answer directly answer the question?

4. Contract grounding
- Does the answer avoid unsupported outside information?

Scoring:

9-10 = Excellent
7-8 = Good
5-6 = Fair
3-4 = Poor
1-2 = Very poor

Return ONLY valid JSON in exactly this format:

{
    "score": 1,
    "explanation": "short explanation"
}
"""