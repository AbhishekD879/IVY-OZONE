const cheerio = require('cheerio'),
  fs = require('fs'),
  dirs = fs.readdirSync('./dist/');

console.log('\x1b[33m%s\x1b[0m', '-----------------------------\n', 'Post build script started...');

dirs.forEach(dir => {

  const file = `./dist/${ dir }/index.html`;

  fs.readFile(file, 'utf8', (err, data) => {
    if (err) {
      return console.log(err);
    }

    const $ = cheerio.load(data);

    $('link[href^=\'styles\']')
      .attr('rel', 'preload')
      .attr('as', 'style')
      .attr('onload', 'this.rel=\'stylesheet\'');

    // tslint:disable-next-line:max-line-length
    $('<script>!function(a){"use strict";var b=function(b,c,d){function j(a){if(e.body)return a();setTimeout(function(){j(a)})}function l(){f.addEventListener&&f.removeEventListener("load",l),f.media=d||"all"}var g,e=a.document,f=e.createElement("link");if(c)g=c;else{var h=(e.body||e.getElementsByTagName("head")[0]).childNodes;g=h[h.length-1]}var i=e.styleSheets;f.rel="stylesheet",f.href=b,f.media="only x",j(function(){g.parentNode.insertBefore(f,c?g:g.nextSibling)});var k=function(a){for(var b=f.href,c=i.length;c--;)if(i[c].href===b)return a();setTimeout(function(){k(a)})};return f.addEventListener&&f.addEventListener("load",l),f.onloadcssdefined=k,k(l),f};"undefined"!=typeof exports?exports.loadCSS=b:a.loadCSS=b}("undefined"!=typeof global?global:this);!function(a){if(a.loadCSS){var b=loadCSS.relpreload={};if(b.support=function(){try{return a.document.createElement("link").relList.supports("preload")}catch(a){return!1}},b.poly=function(){for(var b=a.document.getElementsByTagName("link"),c=0;c<b.length;c++){var d=b[c];"preload"===d.rel&&"style"===d.getAttribute("as")&&(a.loadCSS(d.href,d,d.getAttribute("media")),d.rel=null)}},!b.support()){b.poly();var c=a.setInterval(b.poly,300);a.addEventListener&&a.addEventListener("load",function(){b.poly(),a.clearInterval(c)}),a.attachEvent&&a.attachEvent("onload",function(){a.clearInterval(c)})}}}(this);</script>').insertAfter('link[href^=\'styles\']');

    fs.writeFile(file, $.html(), error => {
      if (error) {
        return console.log(error);
      }

      console.log('\x1b[33m%s\x1b[0m', '-----------------------------\n', 'File: ', file, 'successfully modified...');
    });
  });

});
