class RegexPatterns:
    ICONIFY_ICON = r"^[a-z0-9]+(-[a-z0-9]+)*:[a-z0-9]+(-[a-z0-9]+)*$"
    HEX_COLOR = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
    USERNAME = r"^[a-zA-Z][A-Za-z0-9_]{2,7}$"
    WALLET_BUDGET_NAME = r"^[a-zA-Z0-9][A-Za-z0-9_ -]{1,30}[A-Za-z0-9_]$"