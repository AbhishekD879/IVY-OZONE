import { Component, EventEmitter, Input, Output, AfterViewInit } from '@angular/core';
import { ApiClientService } from '../../client/private/services/http';
import { TinyMCEImageUploadResponse } from '../../client/private/models/tinymce';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '../dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '../../app.constants';

declare var tinymce: any;
declare var $: any;

@Component({
  selector: 'tinymce-editor',
  templateUrl: './tinymce.component.html',
  styleUrls: ['./tinymce.component.scss']
})
export class TinymceComponent implements AfterViewInit {
  /**
   * Current page Info for image upload.
   */
  @Input() pageName: string;
  @Input() pageItemId: string;
  @Input() charLimit: number;
  @Input() minEditorStyles:boolean;
  @Input() readonly: string;

  @Input() initialEditorContent: string;
  @Output() limitExceeded = new EventEmitter();
  @Output() outputEditorData = new EventEmitter();

  /**
   * Generated id for textarea element
   */
  elementId: string;

  /**
   * Link to editor instance to getContent during updates.
   */
  editor: any;

  constructor(
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private apiClientService: ApiClientService
  ) {
    this.elementId = 'tinymce-' + (Math.floor(Math.random() * 100)) + (+(new Date()));

    this.onDataChange = this.onDataChange.bind(this);
    this.onInputChange = this.onInputChange.bind(this);
  }

  addCustomPlugins() {
    tinymce.PluginManager.add('stylebuttons', function (editor, url) {
      ['h1', 'h2', 'h3'].forEach(function (name) {
        editor.addButton('style-' + name, {
          tooltip: 'Toggle ' + name,
          text: name.toUpperCase(),
          onClick: function () { editor.execCommand('mceToggleFormat', false, name); },
          onPostRender: function () {
            const self = this, setup = function () {
              editor.formatter.formatChanged(name, function (state) {
                self.active(state);
              });
            };
            editor.formatter ? setup() : editor.on('init', setup);
          }
        });
      });
    });
  }

  update(value: string): void {
    if (this.editor) {
      this.editor.setContent(value);
    }
  }

  /**
   * Handle change content in textarea
   */
  onDataChange() {
    const content = this.editor.getContent();

    if (content !== undefined) {
      this.outputEditorData.emit(content.replace(/&nbsp;/g, ' '));
    }
  }

  /**
   * Restricts user once the limit is reached
   * @returns - {void}
   */
  onInputChange(editor): void {
    if (this.charLimit) {
      const body = this.editor.getBody();
      const contentLen = (body.innerText || body.textContent).trim().length;
      this.editor.dom.doc.activeElement.contentEditable = true;
      this.limitExceeded.emit('');
      if ((contentLen >= this.charLimit && editor.key !== 'Backspace' && editor.key !== 'Delete')) {
        this.editor.dom.doc.activeElement.contentEditable = false;
        this.limitExceeded.emit(AppConstants.LIMIT_EXCEED_MSG);
      }
    }
  }

  /**
   * Create table from uploaded csv file
   */
  createTableFromFile(data: HttpResponse<TinyMCEImageUploadResponse>): Element {
    const headers = Object.keys(data.body[0]);
    let thead = '';
    headers.forEach(e => {
      thead += '<td>' + e + '</td>';
    });
    const thRow = $('<tr />').attr('class', 'table-header').append(thead);
    const tbody = $('<tbody />').append(thRow);
    $.each(data.body, (e: any) => {
      let td = '';
      $.each(headers, (i: any) => {
        td += '<td>' + data.body[e][headers[i]] + '</td>';
      });

      const trow = $('<tr />').attr('class', 'table-header').append(td);
      tbody.append(trow);
    });
    const result = $('<table />').css('width', '100%').append(tbody);
    return result;
  }

  /**
   * apply editor to rendered textarea
   */
  ngAfterViewInit() {
    const self = this;

    this.addCustomPlugins();
      let addPlugins,addToolBar: any;
      if(!this.minEditorStyles){
        addPlugins = ['BMA, preview, code, link, image, stylebuttons', 'uploadimage', 'textcolor', 'colorpicker', 'table']
        addToolBar = 'bold italic | alignleft aligncenter alignright ' +
        '| bullist numlist | outdent indent | autolink link | image | code ' +
        '| style-h1 style-h2 style-h3 | fontselect | addCollapsePanel makeButton images uploadTable | preview | forecolor backcolor' + '| table | tableStyles' + ' dynamicprice ';
      }else{
        addPlugins = ['BMA, preview, code, link, stylebuttons', 'textcolor', 'colorpicker'];
        addToolBar = 'bold italic | alignleft aligncenter alignright ' +
        '| bullist numlist | outdent indent | autolink link | image | code ' +
        '| style-h1 style-h2 style-h3 ';
      }
    tinymce.init({
      selector: '#' + this.elementId,
      readonly: this.readonly,
      plugins: addPlugins,
      menubar: false,
      skin: 'keystone',
      content_css: ['/assets/lib/tinymce/plugins/bma/content.css'],
      font_formats: 'Arial=Arial,Helvetica,Sans-Serif;Lato=Lato;Helvetica=HelveticaNeue',
      toolbar: addToolBar,
      table_default_attributes: {
        border: '0'
      },
      table_default_styles: {
        width: '100%'
      },
      setup(editor) {
        self.editor = editor;
        editor.on('change', self.onDataChange);
        editor.on('keyup', self.onDataChange);
        editor.on('keydown', self.onInputChange);
      },
      file_browser_callback(field_name, url, type, win) {
        if (!self.pageItemId) {
          self.dialogService.showNotificationDialog({
            title: 'Image Uploader error',
            message: 'Image upload available for created items with ID'
          });

          tinymce.activeEditor.windowManager.close();

          return;
        }

        if (type === 'image') {
          $(`#file-form-input-${self.elementId}`).click();
        }
      }
    });
  }

  handleImageUpload(uploadPage, imagePageId, formData): void {
    this.apiClientService.tinymceService().uploadImage(uploadPage, imagePageId, formData)
      .map((data: HttpResponse<TinyMCEImageUploadResponse>) => {
        return data.body;
      })
      .subscribe((data: TinyMCEImageUploadResponse) => {
        $('.mce-btn.mce-open').parent().find('.mce-textbox').val(data.path);
        this.snackBar.open('Image Uploaded!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Upload error',
          message: error.message
        });
      });
  }

  /**
   * Get the json response of the csv file
   */
  handleTableUpload(uploadPage: string, imagePageId: string, formData: FormData, type: string): void {
    this.apiClientService.tinymceService().uploadImage(uploadPage, imagePageId, formData, type)
      .map((data: HttpResponse<TinyMCEImageUploadResponse>) => {
        const selectedNode = this.editor.selection.getNode();
        selectedNode.append(this.createTableFromFile(data)[0]);
      }).subscribe();
  }

  /**
   * handling the file upload of image and csv file
   */
  handleFileInputChange(event: Event, type?: string): void {
    const uploadPage = this.pageName;
    const imagePageId = this.pageItemId;
    const formData = new FormData();

    formData.append('file', (<HTMLInputElement>event.target).files[0]);

    (type === 'table') ? this.handleTableUpload(uploadPage, imagePageId, formData, type)
      : this.handleImageUpload(uploadPage, imagePageId, formData);

    (<HTMLInputElement>event.target).value = '';
  }
}