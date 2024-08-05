// method used to return text from parent element and exclude text from children
// recipe from https://stackoverflow.com/a/52673846
// not quite useful for framework as it returns text value despite of applied CSS styles
// but as it works – let it be here

var res = '';
var children = arguments[0].childNodes;
for (var n = 0; n < children.length; n++) {
    if (children[n].nodeType === Node.TEXT_NODE) {
        res += ' ' + children[n].nodeValue;
    }
}
return res.trim();
