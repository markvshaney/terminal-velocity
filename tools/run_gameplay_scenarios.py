#!/usr/bin/env python3
"""Run Terminal Velocity symbolic gameplay scenarios and print JSON results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from native_ev.scenario_eval import available_scenarios, run_scripted_scenario  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description='Run Terminal Velocity scripted gameplay scenario evals.')
    parser.add_argument('scenario', nargs='?', default='levo_merchant_first_hop')
    parser.add_argument('--all', action='store_true', help='Run the full symbolic gameplay curriculum')
    parser.add_argument('--list', action='store_true', help='List available scenario names')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')
    args = parser.parse_args()

    if args.list:
        print(json.dumps({'scenarios': available_scenarios()}, indent=2 if args.pretty else None, sort_keys=True))
        return 0
    if args.all:
        results = [run_scripted_scenario(name) for name in available_scenarios()]
        failed = [result for result in results if not result['success']]
        payload = {
            'results': results,
            'summary': {
                'passed': len(results) - len(failed),
                'failed': len(failed),
                'total': len(results),
            },
        }
        print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
        return 0 if not failed else 1

    result = run_scripted_scenario(args.scenario)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
