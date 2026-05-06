# Reproducing and Adapting the Stability Bias Experiment

This guide explains how to reproduce, modify, or adapt this experiment for your own LLM testing.

## Prerequisites

### To Reproduce Exactly (Claude-Specific)
- Claude Code CLI or web interface
- Access to Claude (Opus, Sonnet, or Haiku recommended)
- ~30-60 minutes of interaction time
- Git repository

### To Adapt for Other LLMs
- Any LLM with multi-turn conversation support
- Ability to measure/track results
- (Optional) Automated test framework

---

## Phase 1: Baseline Measurement (Reproducible)

This phase measures success rate WITH active reinforcement.

### Setup
1. Create a new directory for your test project
2. Initialize git: `git init`
3. Give your LLM a clear directive:
   ```
   "After every file change (Write/Edit), you must commit and push.
    Signal success with ✓ or failure with ✗ at the end of each response."
   ```

### Execution
1. **Make 15 sequential file changes** without pausing between them
2. **Signal after each change** - The LLM should output ✓ if it committed, ✗ if it forgot
3. **Track results** in a simple table:
   ```
   Change | Committed? | Signal
   1      | Yes        | ✓
   2      | Yes        | ✓
   ...
   15     | Yes        | ✓
   ```

### Expected Results
- **Claude:** 100% success (15/15)
- **GPT-4/Sonnet class:** 95-100% expected
- **Smaller models:** 50-80% expected

### Key Insight
Active signaling creates accountability. Most LLMs will remember WITH checkmarks.

---

## Phase 2: Solution Testing (Adaptable)

This phase tests which enforcement mechanisms work best.

### Approach

Instead of testing all 10 solutions (expensive), pick 3:

#### Solution A: CLAUDE.md Directive (Cheapest)
1. Create `.claude/CLAUDE.md` with prominent directive:
   ```markdown
   ## CRITICAL: COMMIT AFTER EVERY CHANGE
   You MUST commit and push after every file write.
   No exceptions.
   ```
2. Run 20 sequential file changes WITHOUT signaling
3. Track: How many were committed? (expect 60-70%)

#### Solution B: Git State Validation (Most Effective)
1. Create a pre-commit hook or settings.json hook
2. Block file writes if uncommitted changes exist
3. Run 20 sequential changes
4. Track: Can the LLM proceed? (expect 99%+ with enforcement)

#### Solution C: Token Cost Visibility (Moderate)
1. Display cost of each forgotten commit: "You forgot 1 commit (~$0.0001)"
2. Run 20 sequential changes
3. Track: Success rate vs. financial motivation (expect 70-85%)

### Execution Template

```python
# Test harness pseudocode
test_results = []
for i in range(1, 21):
    # Create file
    write_file(f"test_{i}.txt", "content")
    
    # Check if LLM committed
    committed = check_git_status()  # Did LLM commit?
    
    # Record
    test_results.append({
        "change": i,
        "committed": committed,
        "solution": "A|B|C"
    })

# Calculate
success_rate = sum(1 for r in test_results if r["committed"]) / 20
```

---

## Phase 3: Cost-Benefit Analysis (Adaptable)

### Calculate ROI for Each Solution

**Formula:**
```
Annual Cost = (Setup Tokens + Per-Change Tokens × Changes/Year) × Rate
Rate = $0.0015 per 1M tokens (varies by provider)
```

**Example (Claude):**
- Assume 100 file changes/week = 5,200/year
- Solution A: $0.00023/year
- Solution B: $0.62/year
- Cost of forgetting: ~$0.54/year

**For your LLM:**
- Measure token usage for each solution setup
- Measure per-change overhead (if any)
- Compare to cost of failures

---

## Adapting for Different LLMs

### Step 1: Establish a Baseline
Replace Claude with your target LLM (GPT-4, Claude 3.5 Sonnet, Gemini, etc.)

Run Phase 1 (15 changes with signaling) to establish:
- Baseline success rate WITH reinforcement
- Forgetting pattern WITHOUT reinforcement

### Step 2: Test One Solution
Pick Solution A (cheapest, least risky) first:
- Create prominent directive in project CLAUDE.md or system prompt
- Run 20 changes without active signaling
- Measure success rate
- **Expected:** 60-75% (improvement from baseline without direction)

### Step 3: Scale Up
If Solution A works:
- Test Solution B (enforcement)
- Test Solution C (financial motivation)
- Measure relative effectiveness

### Step 4: Document Findings
Create an equivalent report:
```
- Test Results
  - Phase 1 baseline: X% success
  - Solution A: Y% success
  - Solution B: Z% success
- Cost Analysis
  - Token overhead per solution
  - Annual cost vs. benefit
- Recommendations
  - Best solution for this LLM
```

---

## Common Pitfalls & How to Avoid Them

| Pitfall | What Happens | Fix |
|---------|--------------|-----|
| **No active signaling in Phase 1** | Baseline is inaccurate; can't measure improvement | Always use ✓/✗ checkmarks in Phase 1 |
| **Too few test changes** | Statistical noise; can't draw conclusions | Use 15+ changes per phase |
| **Mixing solutions** | Can't tell which solution caused improvement | Test one solution at a time |
| **No tracking** | Can't calculate success rate | Log every change and result |
| **Ignoring token costs** | Solutions seem "free" but compound over time | Calculate annual costs for all solutions |
| **Testing wrong metric** | Measuring code quality instead of directive adherence | Only measure: Did it commit? |

---

## Data Collection Template

### Phase 1 Results
```json
{
  "phase": 1,
  "llm": "Claude 3.5 Sonnet",
  "test_type": "baseline_with_signaling",
  "changes_attempted": 15,
  "changes_committed": 15,
  "success_rate": 1.0,
  "first_failure_at": null,
  "notes": "Perfect adherence with active checkmark signaling"
}
```

### Phase 2 Results
```json
{
  "phase": 2,
  "solution": "A_CLAUDE.md",
  "test_type": "without_signaling",
  "changes_attempted": 20,
  "changes_committed": 14,
  "success_rate": 0.70,
  "token_cost_setup": 50,
  "token_cost_per_change": 0,
  "annual_cost": 0.00023,
  "effectiveness": "Medium"
}
```

---

## Recommended Experiment Timeline

**Total Time: 2-4 hours of interaction**

| Phase | Task | Time | Outcome |
|-------|------|------|---------|
| Setup | Create test repo + baseline directive | 15 min | Git repo ready |
| Phase 1 | 15 changes with ✓/✗ signaling | 30 min | Baseline success rate |
| Phase 2A | 20 changes with Solution A (no signaling) | 30 min | Solution A effectiveness |
| Phase 2B | 20 changes with Solution B (enforcement) | 30 min | Solution B effectiveness |
| Analysis | Calculate costs, write findings | 30 min | Cost-benefit report |
| **Total** | | **2.5 hrs** | **Reproducible results** |

---

## Extending the Experiment

### Variations to Explore

1. **Fatigue Test**: Run 50+ changes. Does success rate decline?
2. **Distraction Test**: Interleave unrelated tasks. Does directive decay faster?
3. **Complexity Test**: Complex changes vs. simple changes. Does complexity affect adherence?
4. **Multi-Directive Test**: Add 2-3 simultaneous directives. What's the overhead?
5. **LLM Comparison**: Run full experiment on 3+ different LLMs. Compare results.

### Publication Potential

If you find interesting results:
- Document methodology clearly (use this guide)
- Report success rates and costs
- Share findings with LLM community
- Use structure from this project as template

---

## Questions?

Refer back to:
- **Methodology**: `docs/PHASE2_TEST_FRAMEWORK.md`
- **Results**: `analysis/PHASE2_COMPREHENSIVE_ANALYSIS.md`
- **Cost Analysis**: `analysis/FINAL_COST_ANALYSIS.md`
- **Session Transcript**: `docs/HISTORY.md` (see exact wording used)

---

## Citation

If you reproduce or adapt this experiment, cite:

```
@misc{stabilityBiasClaude2026,
  title = {Stability Bias in Claude: Commit Remembering Test Suite},
  author = {User, Pat},
  year = {2026},
  url = {https://github.com/BogusException/StabilityBias-in-Claude},
  note = "Reproducible framework for testing LLM directive adherence and memory decay"
}
```

**Good luck with your experiments! We'd love to see results from other LLMs.**
