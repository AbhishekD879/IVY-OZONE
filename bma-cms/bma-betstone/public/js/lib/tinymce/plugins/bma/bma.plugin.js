(function(){
  var BMARenderer = (function() {
    var menuItems = [
          {
            text  : 'Telephone',
            cssClass : 'phone-text'
          },
          {
            text  : 'Email',
            cssClass : 'email-text'
          },
          {
            text  : 'Warning',
            cssClass : 'warning-text'
          },
          {
            text  : 'Stream icon',
            cssClass : 'stream-link'
          },
          {
            text  : 'Border section',
            cssClass: 'item-panel'
          }
        ],
        buttons = [
          {
            text: 'Green button full',
            cssClass: 'btn-style1 full-width'
          },
          {
            text: 'Blue button full',
            cssClass: 'btn-style2 full-width'
          },
          {
            text: 'Green button half',
            cssClass: 'btn-style1 half-width'
          },
          {
            text: 'Blue button half',
            cssClass: 'btn-style2 half-width'
          },
          {
            text: 'Opt In Button',
            cssClass: 'full-width btn-style2 handle-opt-in hidden'
          }
        ],
        panels = [
          {
            text: 'Collapse-expand panel',
            cssClass: 'toggle-header'
          },
          {
            text: 'Simple panel',
            cssClass: ''
          }
        ];

    function BMARenderer() {
      this.author = 'Invictus Application';
      this.updatedAt = '2015-06-09'; // Please change it to another date/
    }

    BMARenderer.prototype.renderCollapseExpandPanel = function(title, contentOfBody, cssClass) {
      var $p      = $('<p />'      ).html(contentOfBody.length > 0 ? contentOfBody : "&nbsp;"),
          $header = $('<header />' ).attr('class', 'container-header ' + cssClass).text(title),
          $body   = $('<div />'    ).attr('class', 'container-content text-section' ).append($p),
          $panel  = $('<div />'    ).attr('class', 'page-container styled-one-box active')
                                    .append( $header ).append( $body );

      return $panel;
    };

    BMARenderer.prototype.renderButton = function(url, text, target, cssClass, isOptIn) {
      if (!isOptIn && (url.indexOf('tel:') === -1 && url.indexOf('mailto:') === -1) && !isURL(url)) {
        alert('Incorect url string. Be aware that url should start from http://, https://, ftp://, etc.');
        return;
      }

      var $element = $( '<a />' ).attr('class', 'btn ' + cssClass)
                         .attr( 'target', target )
                         .attr( 'href', url );

      const btnText = text || 'Opt In';

      if (isOptIn) {
        $element.html('<span class="btn-status-info"></span><span class="btn-label">' + btnText + '</span>')
      } else {
        $element.text(btnText);
      }

      return $element;
    };

    BMARenderer.prototype.getMenuItems = function(callback) {
      var menu = [];

      $.each(menuItems, function(i, item) {
        menu.push({
          text    : item.text,
          onclick : function(e) {
            var classesToBeRemoved = [];
            $.each(menuItems, function(i, menuItem) {
              if (menuItem.cssClass !== item.cssClass) {
                classesToBeRemoved.push(menuItem.cssClass);
              }
            });
            callback(e, item.cssClass, classesToBeRemoved);
          }
        });
      });

      return menu;
    };

    BMARenderer.prototype.getButtons = function(callback) {
      var menu = [];

      $.each(buttons, function(i, item) {
        menu.push({
          text    : item.text,
          onclick : function(e) { callback(e, item.cssClass, item.text); }
        });
      });

      return menu;
    };

    BMARenderer.prototype.getPanels = function(callback) {
      var menu = [];

      $.each(panels, function(i, item) {
        menu.push({
          text    : item.text,
          onclick : function(e) { callback(e, item.cssClass, item.text); }
        });
      });

      return menu;
    };

    function isURL(url) {
      var strRegex = "^s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+$";
       var re = new RegExp(strRegex);
       return re.test(url);
    }

    return BMARenderer;
  })();

  var bmaRenderer = new BMARenderer();

  // Adds new functionality to tinymce.
  //
  tinymce.PluginManager.add('BMA', BMA);

  /**
   * Adds new functionality for BMA.
   *
   * @param editor - editor of MCE.
   * @param url - url for iframe rendered.
   */
  function BMA(editor, url) {
    editor.addButton('addCollapsePanel', {
      text: 'Create new panel',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getPanels(function(e, cssClass, itemTitle) {
        var initialBM = editor.selection.getBookmark();

        editor.execCommand('mceInsertContent', false, $('<p />').prop('outerHTML') );
        editor.selection.moveToBookmark(initialBM);
        editor.windowManager.open({
          title: itemTitle,
          body: [{
            type   : 'textbox',
            name   : 'title',
            label  : 'Title'
          }],
          onsubmit: function(e) {
            var selectedContent = editor.selection.getContent( { format : 'html' } ),
                $snippet        = bmaRenderer.renderCollapseExpandPanel(e.data.title, selectedContent, cssClass);

            editor.execCommand('mceInsertContent', false, $snippet.prop('outerHTML') );
          }
        });
      })
    });

    editor.addButton('makeButton', {
      text: 'Create bma button',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getButtons(function(e, cssClass, itemTitle) {

        editor.windowManager.open({
          title: itemTitle,
          body: [
            {
              type   : 'textbox',
              name   : 'url',
              label  : 'Url'
            },
            {
              type   : 'textbox',
              name   : 'text',
              label  : 'Text to display'
            },
            {
              type   : 'listbox',
              name   : 'target',
              text   : 'None',
              value  : '',
              label  : 'Target',
              values : [
                {
                  text: 'None',
                  value: ''
                },
                {
                  text: 'New Window',
                  value: '_blank'
                }
              ],
            }
          ],
          onsubmit: function(e){
            var selectedContent = editor.selection.getContent( { format : 'html' } ),
                $snippet        = bmaRenderer.renderButton(
                  e.data.url,
                  e.data.text,
                  e.data.target,
                  cssClass,
                  itemTitle === 'Opt In Button');

            editor.insertContent($snippet.prop('outerHTML'));
          }
        });
      })
    });

    editor.addButton('images', {
      text: 'Styles',
      icon: false,
      type: 'menubutton',
      menu : bmaRenderer.getMenuItems(function(e, cssClass, classesToBeRemoved) {
        var selectedNode = editor.selection.getNode();

        // This should remove content from element.
        //
        if (cssClass === 'stream-link') {
          var $snippet = $('<span />').addClass(cssClass).html('&nbsp;');
          editor.insertContent($snippet.prop('outerHTML'));
        } else if (cssClass === 'item-panel') {
          var $snippet = $('<div />').addClass(cssClass).html('&nbsp;');
          editor.insertContent($snippet.prop('outerHTML'));
        }
        else {
          $.each(classesToBeRemoved, function(i, className) {
            $(selectedNode).removeClass(className);
          });

          $(selectedNode).toggleClass(cssClass);
        }
      })
    });
  }

})();
