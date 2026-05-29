# Automated gameplay learning reference sources

Date added: 2026-05-28

Purpose: reusable reference list for general game-agent/autonomous-task research sources that inform Terminal Velocity automated gameplay learning. These are `automation-design` references, not EV Classic fidelity sources.

## Game-agent / exploration / imitation-learning sources

- **Voyager: An Open-Ended Embodied Agent with Large Language Models**
  - Label: `automation-design`
  - URL: https://arxiv.org/abs/2305.16291
  - Project page: https://voyager.minedojo.org/
  - Use for Terminal Velocity: automatic curriculum, executable skill library, environment feedback, execution-error repair, and self-verification.

- **Go-Explore: a New Approach for Hard-Exploration Problems**
  - Label: `automation-design`
  - URL: https://arxiv.org/abs/1901.10995
  - Use for Terminal Velocity: preserve useful gameplay states/checkpoints, return to promising states cheaply, then explore a new branch from there.

- **General Video Game AI: a Multi-Track Framework for Evaluating Agents, Games and Content Generation Algorithms**
  - Label: `automation-design`
  - URL: https://arxiv.org/abs/1802.10363
  - Use for Terminal Velocity: scenario/evaluator separation, multi-task benchmarking, and generalization checks across varied systems/states.

- **Google Research: Quickly Training Game-Playing Agents with Machine Learning**
  - Label: `automation-design`
  - URL: https://research.google/blog/quickly-training-game-playing-agents-with-machine-learning/
  - Use for Terminal Velocity: short gameplay-loop agents, semantic state/action APIs, and longer tests composed by simple scripting rather than one monolithic player.

- **Video PreTraining (VPT): Learning to Act by Watching Unlabeled Online Videos**
  - Label: `automation-design`
  - URL: https://cdn.openai.com/vpt/Paper.pdf
  - Use for Terminal Velocity: capture small action-labeled user/operator traces and convert them into macros/tests; do not infer EV fidelity from large-scale Minecraft-video results.

## Autonomous web/computer-agent harness references

- **BrowserGym**
  - Label: `automation-design`
  - URL: https://github.com/ServiceNow/BrowserGym
  - Use for Terminal Velocity: task manifests, agent/evaluator separation, run events, artifacts, and reusable environment wrappers.

- **WebArena: A Realistic Web Environment for Building Autonomous Agents**
  - Label: `automation-design`
  - URL: https://arxiv.org/abs/2307.13854
  - Project page: https://webarena.dev/
  - Use for Terminal Velocity: realistic standalone task environments, setup/teardown, expected results, and reproducible validation.

- **OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments**
  - Label: `automation-design`
  - URL: https://arxiv.org/abs/2404.07972
  - Project page: https://os-world.github.io/
  - Use for Terminal Velocity: task setup scripts, execution traces, result getters, artifacts, and validation in a real UI/action environment.

## Guardrail

These sources justify automation architecture and evaluation design only. Original EV Classic runtime observation, decoded EV Classic resources, manuals, and bounded Basilisk traces remain the fidelity sources for game behavior.
