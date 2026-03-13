#!/bin/bash
# CARBONICA Report Generator Wrapper

cd "$(dirname "$0")/.."

case "$1" in
    daily)
        python3 scripts/generate_reports.py --type daily
        ;;
    weekly)
        python3 scripts/generate_reports.py --type weekly
        ;;
    monthly)
        python3 scripts/generate_reports.py --type monthly
        ;;
    all|"")
        python3 scripts/generate_reports.py --type all
        ;;
    *)
        echo "Usage: $0 {daily|weekly|monthly|all}"
        exit 1
        ;;
esac
