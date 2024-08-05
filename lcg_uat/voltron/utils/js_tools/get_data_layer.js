var entrances = dataLayer;

function replacer(key, value) {
    if (key === "gtm.element") {
        return ""
    }
    return value
}

return JSON.stringify(entrances, replacer);
