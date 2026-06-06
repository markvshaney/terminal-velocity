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

## Gameplay automation / game-testing implementation sources

- **Airtest: Cross-Platform UI Automation Framework for Games and Apps**
  - Label: `automation-design`
  - URL: https://github.com/AirtestProject/Airtest
  - Evidence checked: project README says Airtest is a cross-platform UI automation framework for games/apps, uses image recognition to locate UI elements, simulates input/assertions, supports command-line/Python API runs, reports, and screen recording.
  - Use for Terminal Velocity: screen/image-based automation patterns for Basilisk/Godot UI capture loops, assertions, and failure artifacts without requiring engine injection.

- **Poco**
  - Label: `automation-design`
  - URL: https://github.com/AirtestProject/Poco
  - Source checked: `https://raw.githubusercontent.com/AirtestProject/Poco/master/README.rst`.
  - Evidence checked: README describes Poco as a cross-engine UI automation framework for Unity3D, cocos2dx, native apps, and other SDK-integrated engines; it retrieves UI element hierarchy in the game's runtime and provides engine-independent APIs.
  - Use for Terminal Velocity: compare against Godot-side semantic UI hooks and hierarchy/action APIs; not applicable to original EV Classic/Basilisk fidelity unless an external object hierarchy exists.

- **SerpentAI: Python Game Agent Development Kit**
  - Label: `automation-design-lead`
  - URL: https://github.com/SerpentAI/SerpentAI
  - Evidence checked: project README identifies it as a Python game-agent development kit; README also flags pre-alpha status and Linux-only support at the time of that README.
  - Use for Terminal Velocity: architectural lead for screenshot/action-loop game agents; lower priority because of age/pre-alpha status.

- **Wuji: Automatic Online Combat Game Testing Using Evolutionary Deep Reinforcement Learning**
  - Label: `automation-design`
  - URL: https://github.com/NeteaseFuxiRL/wuji
  - Paper/source note: original source code for ASE 2019 distinguished paper.
  - Evidence checked: README says it combines multi-objective evolutionary algorithm (MOEA) and deep reinforcement learning (DRL) to explore game state and discover bugs.
  - Use for Terminal Velocity: bug-finding/exploration design for combat/state-space stress tests; likely overkill for first safe-local TV gameplay automation.

- **Tencent GAutomator**
  - Label: `automation-design-lead`
  - URL: https://github.com/Tencent/GAutomator
  - Evidence checked: README describes an open-source test automation framework for mobile games; interacts with engine elements such as Unity GameObjects; requires SDK integration to interact with game-engine elements.
  - Use for Terminal Velocity: engine-integrated test-agent pattern for Godot-side semantic controls; not useful for original EV Classic/Basilisk automation because it depends on target integration.

- **Stable-Retro / Gym Retro**
  - Label: `automation-design-lead`
  - URL: https://stable-retro.farama.org/
  - Source repository: https://github.com/Farama-Foundation/stable-retro
  - Evidence checked: README describes Stable-Retro as a maintained Gym Retro fork for turning classic video games into Gymnasium reinforcement-learning environments, with multiple supported emulators/platforms.
  - Use for Terminal Velocity: reference for emulator-backed RL environment wrappers and state/action integration; not directly applicable to Classic Mac EV unless a compatible emulator integration exists or is built.

- **GitHub topic indexes: game automation / game testing**
  - Label: `source-discovery-lead`
  - URLs: https://github.com/topics/game-automation and https://github.com/topics/game-testing
  - Evidence checked: search results expose many small Python/OpenCV/mss/PyAutoGUI bots plus broader testing frameworks.
  - Use for Terminal Velocity: discovery surface for implementation examples; individual repos should be inspected before borrowing patterns.

## Guardrail

These sources justify automation architecture and evaluation design only. Original EV Classic runtime observation, decoded EV Classic resources, manuals, and bounded Basilisk traces remain the fidelity sources for game behavior.
