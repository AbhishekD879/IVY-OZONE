import { Component, ViewEncapsulation } from '@angular/core';
import { ListTemplateComponent as ListTemplate } from '@app/lazy-modules/listTemplate/components/list-template.component';

@Component({
  selector: 'list-template',
  templateUrl: 'list-template.component.html',
  styleUrls: ['list-template.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ListTemplateComponent extends ListTemplate {
  }
