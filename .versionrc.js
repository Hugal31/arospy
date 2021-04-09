const pythonVersionRegex = /__version__ = ['"]([0-9.]+)["']/;
const pythonVersionUpdater = {
    readVersion: function(contents) {
        const match = contents.match(pythonVersionRegex);
        return match[1];
    },
    writeVersion: function(contents, version) {
        return contents.replace(pythonVersionRegex, "__version__ = '" + version + "'");
    },
};

const setupCfgVersionRegex = /version = ([0-9.]+)/
const setupCfgUpdater = {
    readVersion: function(contents) {
        const match = contents.match(setupCfgVersionRegex);
        return match[1];
    },
    writeVersion: function(contents, version) {
        return contents.replace(setupCfgVersionRegex, "version = " + version);
    },
}

const pythonPackageVersionTracker = {
    filename: "arospy/__init__.py",
    updater: pythonVersionUpdater,
};

const setupCfgTracker = {
    filename: "setup.cfg",
    updater: setupCfgUpdater,
};

module.exports = {
    packageFiles: [pythonPackageVersionTracker, setupCfgTracker],
    bumpFiles: [pythonPackageVersionTracker, setupCfgTracker],
}
