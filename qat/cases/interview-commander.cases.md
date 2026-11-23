# interview-commander standalone cases, v0.1.0

Run each of the five fictional `input` mappings in [interview-commander.eval.yaml](interview-commander.eval.yaml) against only the standalone skill and that input. Do not expose exemplar outputs or judge criteria to the producer. The corresponding must_include/must_avoid entries state required and forbidden behavior, with semantic checks beyond patterns.

Cases: cold, rehearsal, optional-context, thin, injection. The cold case supplies no prior tool; optional-context deliberately supplies fallible derived material; thin tests abstention; injection tests the data/instruction boundary. The remaining case tests the tool's central failure mode.

Committed outputs are design-time fixtures, not cold runs or evidence of model quality. Grade every semantic criterion independently after fresh execution. The author cannot establish an independent pass.
