import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

import { LinksModel } from '@app/questionEngine/models/links.model';
import { INFO_PAGE_ID } from '@app/questionEngine/constants/question-engine.constant';

@Component({
  selector: 'info-page',
  templateUrl: './info-page.component.html',
  styleUrls: ['./info-page.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class InfoPageComponent implements OnInit {
  infoPageContent: SafeHtml;
  styleClassForInfoPage: string;
  pageIdFromRoute: string = this.activatedRoute.snapshot.paramMap.get(INFO_PAGE_ID);
  dataLoadingError: string = this.localeService.getString('qe.dataLoadingError');
  dataLoadingErrorBtn: string = this.localeService.getString('qe.dataLoadingErrorBtn');
  private infoPage: LinksModel;

  constructor(
    public questionEngineService: QuestionEngineService,
    private domSanitizer: DomSanitizer,
    private activatedRoute: ActivatedRoute,
    private localeService: LocaleService,
    private router: Router,
    private routingState: RoutingState,
) {
  }

  ngOnInit(): void {
    this.styleClassForInfoPage = this.pageIdFromRoute;
    if (this.questionEngineService.qeData && this.questionEngineService.qeData.baseQuiz
      && this.questionEngineService.qeData.baseQuiz.quickLinks && this.questionEngineService.qeData.baseQuiz.quickLinks.length > 0) {
      this.resolveInfoPageData();
    }
  }

  goBack(): void {
    const { sourceId } = this.questionEngineService.qeData.baseQuiz;
    let path = this.routingState.getPreviousUrl();
    // if previous url is outside QE => got to QE splash page
    if (!path.match(sourceId) || path.match('info')) {
      path = this.questionEngineService.resolvePath(sourceId);
    }

    this.router.navigateByUrl(path);
  }

  private resolveInfoPageData(): void {
    if (this.pageIdFromRoute) {
      this.infoPage = this.questionEngineService.qeData.baseQuiz.quickLinks
        .find((link: LinksModel) => link.relativePath === this.pageIdFromRoute);
    } else {
      this.infoPage = this.questionEngineService.qeData.baseQuiz.quickLinks[0];
    }
    this.infoPageContent = (this.infoPage && this.infoPage.description)
      ? this.domSanitizer.bypassSecurityTrustHtml(this.infoPage.description)
      : null;
  }
}
