package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "splashPage")
public class SplashPage extends AbstractEntity implements HasBrand {

  @NotBlank private String title;
  @NotBlank private String brand;
  private String strapLine;
  private String paragraphText1;
  private String paragraphText2;
  private String paragraphText3;
  private String playForFreeCTAText;
  private String seeYourSelectionsCTAText;
  private String seePreviousSelectionsCTAText;
  private String loginToViewCTAText;
  private Filename backgroundSvgFile;
  private String backgroundSvgFilename;
  private Filename logoSvgFile;
  private String logoSvgFilename;
  private Filename footerSvgFile;
  private String footerSvgFilename;
  private String footerText;
  private boolean showPreviousGamesButton;

  public String logoSvgPath() {
    return buildPath(this.getLogoSvgFile());
  }

  public String backgroundSvgPath() {
    return buildPath(this.getBackgroundSvgFile());
  }

  public String footerSvgPath() {
    return buildPath(this.getFooterSvgFile());
  }

  private String buildPath(Filename filename) {
    return filename != null ? filename.relativePath() : "";
  }

  public void clearLogoSvg() {
    this.setLogoSvgFile(null);
    this.setLogoSvgFilename(null);
  }

  public void clearBackgroundSvg() {
    this.setBackgroundSvgFile(null);
    this.setBackgroundSvgFilename(null);
  }

  public void clearFooterSvg() {
    this.setFooterSvgFilename(null);
    this.setFooterSvgFile(null);
  }
}
