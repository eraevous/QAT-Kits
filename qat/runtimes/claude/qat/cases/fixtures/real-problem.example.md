# Example input for real-problem
<!-- Constructed test fixture (not a real conversation or document). Plant each failure mode
     listed in cases/real-problem.eval.yaml here, and keep the key in that file, not in this one. -->

**challenge:** What if the status page keeps showing "all systems normal" for hours after an incident because of the new cache? Nobody would know.

**context:** Project Lantern publishes a public status page. Last week agent-B added a cache in front of it (PR #41, merged by the owner). The cache's time-to-live is set in `config/cache.toml`; nobody in the thread has looked at the value. The status page shows a "last updated" timestamp. There has been no incident since the cache went in.

**authority:** Only the owner accepts risks or closes challenges.

**source:** challenge log entry CH-7, raised by agent-A in the PR #41 review.
