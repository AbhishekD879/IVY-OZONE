import { Component } from '@angular/core';

@Component({
  selector: 'live-serv-iframe',
  template: '<iframe name="push_iframe" ' +
              'id="push_iframe" ' +
              'src="javascript:false" ' +
              'width="22px" height="12px" ' +
              'scrolling="no" ' +
              'frameborder="0"' +
              'marginwidth="0px" ' +
              'marginheight="0px">' +
            '</iframe>'
})
export class LiveServIframeComponent {
}
