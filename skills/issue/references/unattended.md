# Unattended runs (`--no-test`)

Read this before step 1 when the user passed `--no-test`. Nobody is there to answer, so never stop to ask:

- In step 2, take the next issue rather than one that needs the user's decisions, a breaking change, or (when `has_release_tags` is false) a first tag. If `/issue N` names such an issue, take the failure path and put the question in its comment.
- Skip the step 3 model-fit stop; note any mismatch in the report.
- Skip the step 7 pause; review is the last gate before release.
- Any later stop that would ask the user (a decision in step 5 or 6, a breaking change or a version mismatch in step 8, a non-mechanical merge) takes the failure path instead, with the question in its comment.
