def success(foundingYear, status):
    if status.lower() == "inactive":
        return 0
    elif status.lower() == "active":
        return 2020 - foundingYear
    elif status.lower() == "acquired":
        return (2020-foundingYear) * 0.75
    else:
        return 0