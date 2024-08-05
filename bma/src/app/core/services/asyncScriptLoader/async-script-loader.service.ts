import { of as observableOf, Observable, Observer } from "rxjs";
import { map } from "rxjs/operators";
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { WindowRefService } from "../windowRef/window-ref.service";
import environment from "@environment/oxygenEnvConfig";
@Injectable({
  providedIn: "root",
})
export class AsyncScriptLoaderService {
  private loadedFiles: Map<string, boolean> = new Map();
  private isProxiedEnv = false;
  targatedElm: HTMLLinkElement;
  constructor(private windowRef: WindowRefService, private http: HttpClient) {
    this.isProxiedEnv = this.isHashIncluded("main.js");
  }

  loadJsFile(
    fileName: string,
    attrs?: { [key: string]: string },
    idName?: string
  ): Observable<string> {
    if (this.loadedFiles.has(fileName) && this.loadedFiles.get(fileName)) {
      return observableOf(null);
    }
    return Observable.create((observer: Observer<string>) => {
      const script = this.windowRef.document.createElement("script");
      script.type = "text/javascript";
      if (idName) {
        script.id = idName;
      }

      if (attrs) {
        const attributes = Object.keys(attrs);
        attributes.forEach((attribute: string) => {
          script.setAttribute(attribute, attrs[attribute]);
        });
      }

      script.src = fileName;
      script.onload = () => this.onLoad(observer, fileName);
      script.onerror = () => this.onError(observer, fileName);

      this.windowRef.document.body.appendChild(script);
      this.loadedFiles.set(fileName, true);
    });
  }

  loadCssFile(
    fileName: string,
    isHeadAppend?: boolean,
    moduleCss?: boolean
  ): Observable<string> {
    fileName = fileName +  '?' + environment.CSS_Lazy_loadash;
    if (!this.targatedElm) this.targatedElm = this.tagetedElement();
    if (this.loadedFiles.has(fileName) && this.loadedFiles.get(fileName)) {
      return observableOf(null);
    }
    if (moduleCss && !this.isProxiedEnv) {
      fileName = this.getAbsolutePath() + fileName;
    }
    return Observable.create((observer: Observer<string>) => {
      const link = this.windowRef.document.createElement("link");
      link.rel = "stylesheet";
      link.type = "text/css";
      link.media = "all";
      link.href = fileName;
      link.onload = () => this.onLoad(observer, fileName);
      link.onerror = () => this.onError(observer, fileName);
      if (this.targatedElm && moduleCss) {
        this.targatedElm.insertAdjacentElement("afterend", link);
      } else if (isHeadAppend) {
        this.windowRef.document
          .getElementsByTagName("head")[0]
          .appendChild(link);
      } else {
        this.windowRef.document.body.appendChild(link);
      }

      this.loadedFiles.set(fileName, true);
    });
  }
  getAbsolutePath() {
    if(environment.brand === "bma") {
      return environment.CURRENT_PLATFORM === "mobile"
      ? "ClientDist/coralMobile/"
      : "ClientDist/coralDesktop/";
    } else if (environment.brand === "ladbrokes") {
      return environment.CURRENT_PLATFORM === "mobile"
      ? "ClientDist/ladbrokesMobile/"
      : "ClientDist/ladbrokesDesktop/";
    }
  }
  
  isHashIncluded(path): boolean {
    return Array.from(
      this.windowRef.document.body.getElementsByTagName("script")
    ).some((script) => script.src && script.src.includes(path)&& !script.src.includes('ClientDist'));
  }
  tagetedElement(): any {
    return document.querySelector('link[href*="styles."]');
  }
  /**
   * Get svg sprite from cms (S3)
   *
   * @param filePath absolute or relative url to sprite
   */
  getSvgSprite(filePath: string): Observable<string> {
    return this.http
      .get(filePath)
      .pipe(map((data: { [key: string]: string }) => data.content));
  }

  loadSvgIcons(fileName: string, isLoaded: boolean = true): Observable<string> {
    if (this.loadedFiles.has(fileName) && isLoaded) {
      return observableOf(null);
    }

    const httpOptions = {
      responseType: "text" as const,
    };

    return this.http.get(fileName, httpOptions).pipe(
      map((data: string) => {
        this.loadedFiles.set(fileName, true);
        return data;
      })
    );
  }

  private onError(observer, fileName: string): void {
    this.loadedFiles.set(fileName, false);
    observer.error(`Fail to Load ${fileName}`);
    observer.complete();
  }

  private onLoad(observer, fileName: string): void {
    observer.next(fileName);
    observer.complete();
  }
}
