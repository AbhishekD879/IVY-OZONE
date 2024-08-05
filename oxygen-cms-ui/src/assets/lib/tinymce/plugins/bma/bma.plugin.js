(function () {
  let buttonBody = [
    {
      type: 'textbox',
      name: 'url',
      label: 'Url'
    },
    {
      type: 'textbox',
      name: 'text',
      label: 'Text to display'
    },
    {
      type: 'listbox',
      name: 'target',
      text: 'None',
      value: '',
      label: 'Target',
      values: [
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
  ];
  let betPackButtonBody = [
    {
      type: 'textbox',
      name: 'text',
      label: 'Text to display'
    }
  ];
  var BMARenderer = (function () {
    var menuItems = [
      {
        text: 'Telephone',
        cssClass: 'phone-text'
      },
      {
        text: 'Email',
        cssClass: 'email-text'
      },
      {
        text: 'Warning',
        cssClass: 'warning-text'
      },
      {
        text: 'Stream icon',
        cssClass: 'stream-link'
      },
      {
        text: 'Border section',
        cssClass: 'item-panel'
      },
      {
        text: 'Line break',
        cssClass: 'line-break'
      }
    ],
      tableMenuItems = [
        {
          text: 'Hightlight Row',
          cssClass: 'hightlight-row'
        },
        {
          text: 'Un-Hightlight Row',
          cssClass: 'un-hightlight-row'
        },
        {
          text: 'Fix Table Width',
          cssClass: 'fix-table-width'
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
        },
        {
          text: 'Bet Pack button full',
          cssClass: 'btn-style1 full-width bet-pack-btn'
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
        },
        {
          text: 'Section Header',
          cssClass: 'sub-header'
        }
      ],
      dynamicPricingButtons = [
        {
          text: 'Dynamic Button',
          cssClass: 'dynamic-btn-style .btn'
        }
      ];

    function BMARenderer() {
      this.author = 'Invictus Application';
      this.updatedAt = '2015-06-09'; // Please change it to another date/
    }

    /**
     * Generates HTML markup for accordion header
     * @param {String} title - header titlle
     * @param {String} cssClass - CSS class to add for header element
     */
    function generateAccordionHeader(title, cssClass) {
      const $titleSpan = $('<span />').attr('class', 'left-title-text').text(title),
        $leftSide = $('<div />').attr('class', 'left-side-element-js').append($titleSpan),
        $header = $('<header />').attr('class', 'container-header ' + cssClass).append($leftSide);
      return $header;
    }

    /**
     * Generates HTML markup for accordion body
     * @param {String} contentOfBody 
     */
    function generateAccordionBody(contentOfBody) {
      var $contentDiv = $('<div >').attr('class', 'container-inside-text').html(contentOfBody.length > 0 ? contentOfBody : "&nbsp;"),
        $containerContenArticle = $('<article />').attr('class', 'container-content text-section').append($contentDiv);
      return $containerContenArticle;
    }

    BMARenderer.prototype.renderCollapseExpandPanel = function (title, contentOfBody, cssClass) {
      var $p = $('<p />').html(contentOfBody.length > 0 ? contentOfBody : "&nbsp;"),
        $header = generateAccordionHeader(title, cssClass),
        $body = generateAccordionBody(contentOfBody)
      $accordionBodySection = $('<section >').attr('class', 'page-container no-header is-expanded').append($header).append($body)
      $accordion = $('<div />').attr('class', 'accordion-element-js').append($accordionBodySection);

      return $accordion;
    };

    BMARenderer.prototype.renderButton = function (url, text, target, cssClass, itemTitle) {
      const isOptIn = itemTitle === 'Opt In Button';
      var $element = $('<a />').attr('class', 'btn ' + cssClass);
      if (url !== 'NULL') {
        if (!isOptIn && (url.indexOf('tel:') === -1 && url.indexOf('mailto:') === -1) && !isURL(url)) {
          alert('Incorect url string. Be aware that url should start from http://, https://, ftp://, etc.');
          return;
        } else {
          $element.attr('target', target).attr('href', url);
        }
      }

      
      if(!text){
        itemTitle === 'Bet Pack button full'?btnText ='Bet Pack':btnText = 'Opt In'
     }else{
       btnText = text;
     }

      if (isOptIn) {
        $element.html('<span class="btn-status-info"></span><span class="btn-label">' + btnText + '</span>')
      } else {
        $element.text(btnText);
      }

      return $element;
    };

    BMARenderer.prototype.renderDynamicButton = function (selectionId, cssClass) {
      $emptyDivTag = $('<div />').attr('contenteditable', 'true').attr('id', 'textarea').html('<p>&nbsp;</p>');
      var $element = $('<button />').attr('class', 'btn ' + cssClass).attr('id', `dynamicbtn-${selectionId}`);
      const btnText = `${selectionId} - N/A`;
      $element.text(btnText);
      $emptyTag = $('<p />').attr('id', 'empty');
      var $dynamicBtn = $('<p />').attr('id', 'container-el').append($emptyDivTag).append($element).append($emptyTag);
      return $dynamicBtn;
    };

    BMARenderer.prototype.getMenuItems = function (callback) {
      var menu = [];

      $.each(menuItems, function (i, item) {
        menu.push({
          text: item.text,
          onclick: function (e) {
            var classesToBeRemoved = [];
            $.each(menuItems, function (i, menuItem) {
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

    BMARenderer.prototype.getTableMenuItems = function (callback) {
      var tableMenu = [];
      $.each(tableMenuItems, function (i, item) {
        tableMenu.push({
          text: item.text,
          onclick: function (e) {
            callback(e, item.cssClass);
          }
        });
      });
      return tableMenu;
    };

    BMARenderer.prototype.getButtons = function (callback) {
      var menu = [];

      $.each(buttons, function (i, item) {
        menu.push({
          text: item.text,
          onclick: function (e) { callback(e, item.cssClass, item.text); }
        });
      });

      return menu;
    };

    BMARenderer.prototype.getPanels = function (callback) {
      var menu = [];

      $.each(panels, function (i, item) {
        menu.push({
          text: item.text,
          onclick: function (e) { callback(e, item.cssClass, item.text); }
        });
      });

      return menu;
    };

    BMARenderer.prototype.getDynamicPriceButtons = function (callback) {
      var menu = [];
      $.each(dynamicPricingButtons, function (index, dynamicPricingButtonItem) {
        menu.push({
          text: dynamicPricingButtonItem.text,
          onclick: function (event) { callback(event, dynamicPricingButtonItem.cssClass, dynamicPricingButtonItem.text); }
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
      menu: bmaRenderer.getPanels(function (e, cssClass, itemTitle) {
        var initialBM = editor.selection.getBookmark();

        editor.execCommand('mceInsertContent', false, $('<p />').prop('outerHTML'));
        editor.selection.moveToBookmark(initialBM);
        editor.windowManager.open({
          title: itemTitle,
          body: [{
            type: 'textbox',
            name: 'title',
            label: 'Title'
          }],
          onsubmit: function (e) {
            var selectedContent = editor.selection.getContent({ format: 'html' }),
              $snippet = bmaRenderer.renderCollapseExpandPanel(e.data.title, selectedContent, cssClass);

            editor.execCommand('mceInsertContent', false, $snippet.prop('outerHTML'));
          }
        });
      })
    });

    editor.addButton('makeButton', {
      text: 'Create bma button',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getButtons(function (e, cssClass, itemTitle) {

        editor.windowManager.open({
          title: itemTitle,
          body: itemTitle === 'Bet Pack button full' ? betPackButtonBody : buttonBody,
          onsubmit: function (e) {
            let url;
            url = e.data && (e.data.url || e.data.url == '') ? e.data.url : 'NULL';
            var selectedContent = editor.selection.getContent({ format: 'html' }),
              $snippet = bmaRenderer.renderButton(
                url,
                e.data.text,
                e.data.target,
                cssClass,
                itemTitle);

            editor.insertContent($snippet.prop('outerHTML'));
          }
        });
      })
    });

    editor.addButton('uploadTable', {
      text: 'Upload Table',
      icon: false,
      type: 'button',
      onclick: function (e) {
        $(e.currentTarget.parentElement).find("input[name='table']").trigger('click');
      }
    });

    editor.addButton('images', {
      text: 'Styles',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getMenuItems(function (e, cssClass, classesToBeRemoved) {
        var selectedNode = editor.selection.getNode();

        // This should remove content from element.
        //
        if (cssClass === 'stream-link') {
          var $snippet = $('<span />').addClass(cssClass).html('&nbsp;');
          editor.insertContent($snippet.prop('outerHTML'));
        } else if (cssClass === 'item-panel') {
          var $snippet = $('<div />').addClass(cssClass).html('&nbsp;');
          editor.insertContent($snippet.prop('outerHTML'));
        } else if (cssClass === 'line-break') {
          $(selectedNode).append('<hr/><br/>');
        } else {
          $.each(classesToBeRemoved, function (i, className) {
            $(selectedNode).removeClass(className);
          });

          $(selectedNode).toggleClass(cssClass);
        }
      })
    });

    editor.addButton('tableStyles', {
      text: 'Table Styles',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getTableMenuItems(function (e, cssClass) {
        var selectedNode = editor.selection.getNode();
        tempNode = editor.selection.getNode();
        if (cssClass === 'hightlight-row') {
          $(selectedNode).closest('tr').addClass('hightlight-row');
        } else if (cssClass === 'un-hightlight-row') {
          $(selectedNode).closest('tr').removeClass('hightlight-row');
        } else if (cssClass === 'fix-table-width') {
          $(selectedNode).closest('table').toggleClass('fixed-table');
        }
      })
    });

    editor.addButton('dynamicprice', {
      text: 'Add dynamic price',
      icon: false,
      type: 'menubutton',
      menu: bmaRenderer.getDynamicPriceButtons(function (event, cssClass, itemTitle) {
        editor.execCommand('mceInsertContent', false, $('<p />').prop('outerHTML'));
        editor.windowManager.open({
          title: itemTitle,
          body: [
            {
              type: 'textbox',
              name: 'selection',
              label: 'Selection Id'
            }],
          onsubmit: function (selectionIdDataInput) {
            $snippet = bmaRenderer.renderDynamicButton(
              selectionIdDataInput.data.selection,
              cssClass);
            editor.insertContent($snippet.prop('outerHTML'));
          }
        })
      })
    });
  }
})();
