import { Component } from '@angular/core';

import { FooterComponent as AppFooterComponent } from '@app/questionEngine/components/shared/footer/footer.component';

@Component({
  selector: 'qe-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})

export class FooterComponent extends AppFooterComponent {
}
