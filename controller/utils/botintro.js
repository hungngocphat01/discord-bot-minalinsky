const fs = require('fs');
let json = fs.readFileSync("package.json", { encoding: "utf-8" });
_package = JSON.parse(json);

module.exports = {
    getHeader() {
        return `
${_package['styled-name']}
Version ${_package['version']}
By ${_package['author']}
Last updated: ${_package['last-updated']}
============================================`.trim();
    }
}