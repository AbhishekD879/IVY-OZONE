import { Component } from '@angular/core';
import { SportMainComponent as CoreSportMainComponent } from '@app/sb/components/sportMain/sport-main.component';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';

@Component({
  selector: 'sport-main-component',
  styleUrls: ['sport-main.component.scss'],
  templateUrl: 'sport-main.component.html'
})
export class SportMainComponent extends CoreSportMainComponent {

  get sportDetailPage(): string {
    return this.isSportDetailPage ? 'eventDetailsPage' : '';
  }
  set sportDetailPage(value:string){}

  protected shouldNavigatedToTab() {
    return this.isHomeUrl();
  }

  protected setDefaultTab(sportTabs: ISportConfigTab[]){
    const matchesTab: ISportConfigTab = sportTabs.find((tab: ISportConfigTab) => tab.name === 'matches' && !tab.hidden);
    if (matchesTab) {
      this.defaultTab = matchesTab.name;
    } else {
      const firstTab = sportTabs.find((tab: ISportConfigTab) => !tab.hidden);
      this.defaultTab = firstTab && firstTab.name;
    }
  }

  protected filterTabs(sportTabs: ISportConfigTab[]): ISportConfigTab[] {
    sportTabs.forEach((tab: ISportConfigTab, index: number) => {
      if ((tab.id === 'tab-matches' || tab.id === 'tab-live') && this.sportId !== '18') {
        tab.hidden = false;
      }
      if(tab.id === 'tab-matches') {
        tab.url = this.defaultTab ? `/sport/${this.sportPath}/matches/today` : `/sport/${this.sportPath}`;
      }
    // this.defaultTab = 'matches';
    //  const firstTab = sportTabs.find((tab: ISportConfigTab) => !tab.hidden);
    //  this.defaultTab = firstTab && firstTab.name;
    });
   this.setDefaultTab(sportTabs);
   
   if(this.sportId!=='18'){
    if (!sportTabs.find(sportTab => sportTab.id === 'tab-live')) {
      sportTabs.unshift({
        id: 'tab-live',
        name: 'live',
        label: 'sb.tabsNameInPlay',
        url: `/sport/${this.sportPath}/live`,
        hidden: false,
        sortOrder: 1
      });
    }
  }

    return sportTabs;
  }
}
