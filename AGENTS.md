# Reader Improvement Lab

Read the [workspace policy](../../../../../AGENTS.md), [public-project policy](../../../../../docs/okf/agent-policies/public-project.md), and [investigation design](knowledge/design.md) before changing this project.

The user explicitly requested a self-contained public repository of findings. The research under `knowledge/` and the structured records under `data/` are this project's primary deliverable and canonical sources; link to them from the workspace rather than maintaining a second copy.

Record the examined artifact SHA-256 or upstream commit, source URL, observation date, evidence type, and limitations for every material finding. Static presence, upstream documentation, a proposed improvement, and a reproduced runtime defect are different claims. Unknown does not mean absent. The supplied APK has unverified provenance; its behavior cannot establish a defect in the official Play build.

Keep APKs, extracted proprietary source, credentials, user documents, and raw local configuration outside the public repository. Publish original analysis, minimal diagnostic excerpts, public-source permalinks, and synthetic fixtures. Preserve upstream licenses in contribution patches.

Test Android only on the explicitly selected disposable audit AVD. Use an explicit ADB serial; never select a personal device implicitly. Each runtime record names the build, fixture, environment, steps, actual result, and supporting evidence.

Use the validation commands in `README.md`. Successful fixture or repository validation does not count as an application test. Contributions to other readers require their own focused verification and are tracked separately from proposals.
