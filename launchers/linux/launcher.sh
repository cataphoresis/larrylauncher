#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="${BASH_SOURCE[0]%/*}"
[[ "$SCRIPT_DIR" == "${BASH_SOURCE[0]}" ]] && SCRIPT_DIR="."
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BOOTSTRAP="$ROOT_DIR/runtime/larrybootstrap/bootstrap.sh"
REPORT_DIR="$ROOT_DIR/runtime/larrybootstrap/platforms/linux/reports"
ACTION="menu"

usage() {
    printf '%s\n' \
        'Usage: ./larry-launcher [--action menu|install|verify|audit|reports]' \
        '' \
        'With no arguments, LarryLauncher starts its interactive menu.'
}

while (( $# > 0 )); do
    case "$1" in
        --action) [[ $# -ge 2 ]] || { printf '[FAIL] --action requires a value.\n' >&2; exit 2; }; ACTION="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) printf '[FAIL] Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
done

[[ "$(uname -s)" == "Linux" ]] || { printf '[FAIL] This launcher package requires Linux.\n' >&2; exit 1; }
[[ -x "$BOOTSTRAP" ]] || { printf '[FAIL] Bundled LarryBootstrap runtime is missing.\n' >&2; exit 1; }

show_banner() {
    printf '\n+----------------------------------------------------------+\n'
    printf '|  L A R R Y L A U N C H E R  //  NODE ONLINE            |\n'
    printf '+----------------------------------------------------------+\n'
    printf '|  SYSTEM  %-18s USER     %-17s|\n' "Linux" "$(id -un)"
    printf '|  HOST    %-18s ACTION   %-17s|\n' "$(hostname -s)" "$ACTION"
    printf '+----------------------------------------------------------+\n'
}

show_reports() {
    printf '\nRecent Reports\n==============\n'
    [[ -d "$REPORT_DIR" ]] || { printf '[INFO] No report directory exists yet.\n'; return 0; }
    find "$REPORT_DIR" -maxdepth 2 -type f -print 2>/dev/null | sort -r | head -n 10
    printf '[INFO] %s\n' "$REPORT_DIR"
}

run_action() {
    case "$1" in
        install) "$BOOTSTRAP" full ;;
        verify|audit) "$BOOTSTRAP" audit ;;
        reports) show_reports ;;
        exit) return 0 ;;
        *) printf '[FAIL] Unsupported action: %s\n' "$1" >&2; return 2 ;;
    esac
}

show_banner
if [[ "$ACTION" != "menu" ]]; then run_action "$ACTION"; exit $?; fi

while true; do
    printf '\n[1] Install / reconcile workstation\n[2] Verify configuration\n[3] Run system audit\n[4] List recent reports\n[Q] Disconnect\n\n'
    read -r -p 'SELECT: ' selection
    case "$selection" in
        1) read -r -p 'Run the full bootstrap? [y/N] ' confirmation; [[ "$confirmation" =~ ^[Yy]$ ]] || { printf '[INFO] Install cancelled.\n'; continue; }; selected_action="install" ;;
        2) selected_action="verify" ;;
        3) selected_action="audit" ;;
        4) selected_action="reports" ;;
        q|Q) printf '[INFO] Carrier dropped. Goodbye.\n'; exit 0 ;;
        *) printf '[WARN] Unknown selection.\n'; continue ;;
    esac
    run_action "$selected_action"
done
