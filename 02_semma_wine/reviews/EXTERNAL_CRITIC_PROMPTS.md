# External critique protocol: SEMMA

## Evidence status

**No Claude or GPT-5 critique has been obtained in this session.** The two internal passes in INTERNAL_REVISIONS.md are current-assistant self-review. They do not meet the assignment's requirement to use Claude or GPT-5. Do not relabel them. Obtain the external reviews below, preserve genuine responses, revise, and rerun.

Use a model explicitly permitted by the assignment. Save the exact model label shown by the provider, date, conversation/export reference, input section version/hash, full prompt, full response, and resulting changes. If the professor accepts a different model, record that approval separately. A fabricated conversation or model name is not valid evidence.

The expert persona is role-play for a demanding review. It is not a factual claim that a model has professional credentials or awards. Never treat persona confidence as evidence. Verify source claims and code independently.

## Common review instructions

Provide REPORT.md, the relevant notebook cells or analysis.py section, the source manifest, and the actual CSV/JSON metrics or figures needed to assess the section. Do not send only the conclusion. Ask the critic to identify unsupported claims, omitted subtasks, leakage, source confusion, code errors, fragile assumptions, and missing submission evidence. Require issue severity and exact correction locations.

## Section 1: Sample

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Sample section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Sample section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

## Section 2: Explore

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Explore section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Explore section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

## Section 3: Modify

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Modify section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Modify section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

## Section 4: Model

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Model section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Model section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

## Section 5: Assess

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Assess section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Assess section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

## Section 6: Delivery extension

### Round 1 prompt

```text
Role-play as a world-renowned speaker and authority on SEMMA, with the standards of an author of multiple award-winning books on the subject. This is a fictional reviewer persona, not a claim of real credentials. Be skeptical and precise.

Review only the Delivery extension section of my SEMMA project in the attached report and code, while checking its dependencies on adjacent stages. The professor requires every stage and subtask, detailed artifacts, verification, multiple critique revisions, Colab delivery, an article, and a recorded walkthrough. Distinguish required methodology tasks from extra delivery activities.

For every task, state complete / partial / missing, quote its evidence location, and identify what you cannot verify. Check the technical reasoning and executable code against the supplied outputs. Identify leakage, misleading causal language, invalid metrics, unsupported dataset claims, and source/template mismatches. Propose specific edits and tests, ranked critical / major / minor. Do not invent execution, publications, SAS runs, human verification, or business results. Explain which issues block acceptance. Finish with a numbered revision checklist.

Attached evidence: [paste current section, exact code cells, and actual artifacts here].
```

Apply the corrections, preserve the original response, and save the revised section as revision 1 with its input/output hashes.

### Round 2 prompt

```text
Continue the same demanding SEMMA expert reviewer role. Audit the revised Delivery extension section against the original Round 1 issues, the full task list, and the actual rerun outputs.

Return an issue-resolution table: original issue, original location, correction, evidence, and resolved / partial / unresolved. Recheck mathematics, data leakage, reproducibility, phase boundaries, source alignment, and whether claims match execution. Find new defects introduced by the revision. If the section is insufficient, require another revision; do not grant a pass because a response sounds polished. Keep missing Claude/GPT-5 evidence, manual student verification, Colab execution, publication, and video evidence explicitly pending unless the attachments actually establish them.

Attached: [Round 1 prompt/response, revision 1, change log, and rerun evidence].
```

Implement the second-round corrections, rerun affected work, and store final artifacts. Do not change the frozen test-set decisions to improve a reported score. If the experimental design materially changes after looking at test results, acknowledge it and obtain a new holdout for confirmatory claims.

