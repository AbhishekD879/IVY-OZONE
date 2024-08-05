import {
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
  EventEmitter,
  Output,
  ChangeDetectionStrategy,
  ChangeDetectorRef
} from '@angular/core';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { SVG_TEAM_KIT } from './svg-team-kit.enums';

@Component({
  selector: 'svg-team-kit',
  templateUrl: './svg-team-kit.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SvgTeamKitComponent implements OnInit {
  @ViewChild('teamKit', { static: true }) teamKitRef: ElementRef;
  @Input() fileName: string;
  @Output() readonly isTeamKitAvailable: EventEmitter<boolean> = new EventEmitter<boolean>();

  svgIsLoaded: boolean = false;
  svgIcon: string;

  constructor(
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private changeDetecterRef: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.svgIcon = `#${this.fileName}`;
    this.asyncScriptLoaderService
      .loadSvgIcons(`/assets/images/svg/team-kits/${this.fileName}.svg`, false)
      .subscribe((data: string) => {
        const parser = new DOMParser(),
          svg = parser.parseFromString(data, 'image/svg+xml');
        this.teamKitRef.nativeElement.append(svg.documentElement);
        this.svgIsLoaded = true;
        if (!data.endsWith(SVG_TEAM_KIT.SVG)) {
          this.svgIsLoaded = false;
          this.isTeamKitAvailable.emit(false);
        }
        this.changeDetecterRef.markForCheck();
    }, () => {
      this.isTeamKitAvailable.emit(false);
    });
  }

}
