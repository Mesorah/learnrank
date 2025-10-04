global.gettext = (s) => s;

global.interpolate = (fmt, vars) => {
    let result = fmt;

    for (const key in vars) {
        result = result.replace(`%(${key})s`, vars[key]);
    }

    return result;
};

